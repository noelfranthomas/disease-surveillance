import logging
from pprint import pprint

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
EXA_API_URL = "https://api.exa.ai/search"

def exa_search(
    query,
    api_key,
    category="research paper",
    search_type="neural",
    use_autoprompt=False,
    num_results=10
):
    """
    Basic search function for Exa that returns JSON results.
    """
    payload = {
        "query": query,
        "useAutoprompt": use_autoprompt,
        "type": search_type,
        "category": category,
        "numResults": num_results,
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    logging.info(f"[Exa Search] Category={category}, Query='{query}'")

    try:
        response = requests.post(EXA_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for category={category}: {e}")
        return {"error": str(e)}
    except ValueError as e:
        logging.error(f"JSON parse error for category={category}: {e}")
        return {"error": "Invalid JSON response from server"}

def aggregator_search(
    query,
    api_key,
    categories=None,
    search_type="neural",
    use_autoprompt=False,
    num_results=5
):
    """
    1) Searches across multiple categories in Exa (e.g., 'research paper', 'news', 'pdf').
    2) Aggregates all results into a single list or dictionary for easy consumption.

    :param query: Main query string
    :param api_key: Exa API key
    :param categories: List of categories to search, e.g. ['research paper', 'news', 'pdf']
    :param search_type: 'neural', 'keyword', or 'auto'
    :param use_autoprompt: Whether to use Exa's autoprompt
    :param num_results: Number of results per category
    :return: A combined dictionary of { category_name: search_results }
    """
    if categories is None:
        categories = ["research paper", "news", "pdf"]  # default categories

    all_results = {}

    for cat in categories:
        results = exa_search(
            query=query,
            api_key=api_key,
            category=cat,
            search_type=search_type,
            use_autoprompt=use_autoprompt,
            num_results=num_results
        )
        all_results[cat] = results

    return all_results


def synonym_expansion_search(
    original_query,
    exa_api_key,
    openai_api_key,
    synonyms_count=3,
    num_results=5
):
    """
    1) Use an LLM to generate synonyms or related phrases for the query.
    2) Perform multiple searches using these expansions.
    3) Return combined results.

    :param original_query: The user-provided query
    :param exa_api_key: Exa API key
    :param openai_api_key: OpenAI API key
    :param synonyms_count: How many synonym/related variations to generate
    :param num_results: Number of results per variation
    :return: dict with structure { "variations": [ { "query": q, "results": ... }, ... ] }
    """
    import openai

    openai.api_key = openai_api_key

    # Ask an LLM to produce synonyms/related expansions
    prompt = (
        f"Generate {synonyms_count} different synonyms or related search phrases "
        f"for the query: '{original_query}'. "
        f"Return them in a bullet list."
    )

    try:
        llm_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
    except Exception as e:
        logging.error(f"OpenAI Error generating synonyms: {e}")
        return {"error": str(e)}

    # Extract synonyms from the LLM response
    expansions_raw = llm_response.choices[0].message.content.strip()
    # Simple parse: each line is one suggestion
    expansions = []
    for line in expansions_raw.split("\n"):
        if line.strip():
            expansions.append(line.strip("- ").strip())

    # We also want to include the original query as one of the variations
    all_queries = [original_query] + expansions

    results_data = {"variations": []}

    # Run Exa search for each query
    for q in all_queries:
        search_res = exa_search(q, exa_api_key, category="research paper", num_results=num_results)
        results_data["variations"].append({
            "query": q,
            "results": search_res
        })

    return results_data


def iterative_search(
    initial_query,
    exa_api_key,
    openai_api_key,
    steps=2,
    num_results=5
):
    """
    1) Search once with the initial query.
    2) Summarize or extract keywords from the results using GPT.
    3) Use those extracted keywords to form a new query and search again.
    4) Repeat for 'steps' times.

    :param initial_query: The starting query
    :param exa_api_key: Exa API key
    :param openai_api_key: OpenAI API key
    :param steps: How many times to iterate
    :param num_results: number of results each step
    :return: A dict containing all search results from each iteration
    """
    import openai

    openai.api_key = openai_api_key

    all_results = {}
    current_query = initial_query

    for step in range(1, steps + 1):
        logging.info(f"=== Iteration {step} | Query: {current_query} ===")
        # 1) Execute the search
        results = exa_search(
            query=current_query,
            api_key=exa_api_key,
            category="research paper",
            num_results=num_results
        )
        all_results[f"step_{step}"] = {
            "query": current_query,
            "results": results
        }

        # 2) Summarize or pick out key terms for the next iteration
        # Extract the textual snippet from results (just a simplistic approach)
        snippet_texts = []
        if "result" in results:
            for r in results["result"]:
                snippet_texts.append(r.get("snippet", ""))

        combined_snippets = " ".join(snippet_texts)[:4000]  # keep under GPT token limits

        # Prompt GPT for next-step query
        prompt = (
            "Here is a collection of text from some search results:\n\n"
            f"{combined_snippets}\n\n"
            "From this text, suggest a new search query that might lead to additional insights. "
            "Return only the query text."
        )

        try:
            llm_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            new_query = llm_response.choices[0].message.content.strip()

            # If the LLM doesn't produce anything sensible, just break out
            if not new_query:
                logging.warning("No new query generated. Stopping iteration.")
                break

            current_query = new_query
        except Exception as e:
            logging.error(f"Error generating next query: {e}")
            break

    return all_results


if __name__ == "__main__":
    exa_api_key = "YOUR_EXA_API_KEY"
    openai_api_key = "YOUR_OPENAI_API_KEY"

    # 1. Multi-Category Aggregation
    print("=== Multi-Category Aggregation ===")
    aggr_results = aggregator_search(
        query="Mpox data trends",
        api_key=exa_api_key,
        categories=["research paper", "news", "pdf"],  # or any categories you want
        num_results=3
    )
    pprint(aggr_results)

    # 2. Synonym / Expansion-based Search
    print("\n=== Synonym Expansion Search ===")
    synonyms_results = synonym_expansion_search(
        original_query="Mpox data trends",
        exa_api_key=exa_api_key,
        openai_api_key=openai_api_key,
        synonyms_count=2,
        num_results=3
    )
    pprint(synonyms_results)

    # 3. Iterative Search
    print("\n=== Iterative Multi-step Search ===")
    iterative_results = iterative_search(
        initial_query="Mpox data trends",
        exa_api_key=exa_api_key,
        openai_api_key=openai_api_key,
        steps=2,
        num_results=3
    )
    pprint(iterative_results)
