class Paper:

    def __init__(self, study_id, title, authors, publication_date, journal, location, sample_size,
                 demographics, reported_symptoms, transmission_routes, vaccination_data,
                 outcomes, study_methods, key_findings, risk_factors, recommendations):
        """
        Initialize the data schema with attributes for mpox research papers and studies.

        Parameters:
        - study_id (str): Unique identifier for the study or paper.
        - title (str): Title of the paper or study.
        - authors (list): List of authors.
        - publication_date (str): Date the paper was published (format: YYYY-MM-DD).
        - journal (str): Name of the journal or source.
        - location (str): Geographic focus of the study (e.g., "Sub-Saharan Africa").
        - sample_size (int): Number of subjects included in the study.
        - demographics (dict): Demographics of the population (e.g., {"age_range": "18-45", "gender_ratio": "50:50"}).
        - reported_symptoms (list): Symptoms reported in the study.
        - transmission_routes (list): Identified transmission routes (e.g., ["close contact", "respiratory droplets"]).
        - vaccination_data (dict): Data on vaccination (e.g., {"coverage": 70, "efficacy": 85}).
        - outcomes (dict): Outcome statistics (e.g., {"recovered": 95, "deceased": 5}).
        - study_methods (str): Methods used in the study (e.g., "retrospective cohort analysis").
        - key_findings (str): Summary of key findings.
        - risk_factors (list): Identified risk factors.
        - recommendations (str): Recommendations provided in the study.
        """
        self.study_id = study_id
        self.title = title
        self.authors = authors
        self.publication_date = publication_date
        self.journal = journal
        self.location = location
        self.sample_size = sample_size
        self.demographics = demographics
        self.reported_symptoms = reported_symptoms
        self.transmission_routes = transmission_routes
        self.vaccination_data = vaccination_data
        self.outcomes = outcomes
        self.study_methods = study_methods
        self.key_findings = key_findings
        self.risk_factors = risk_factors
        self.recommendations = recommendations

    def to_dict(self):
        """
        Converts the data schema object into a dictionary.
        """
        return {
            "Study ID": self.study_id,
            "Title": self.title,
            "Authors": self.authors,
            "Publication Date": self.publication_date,
            "Journal": self.journal,
            "Location": self.location,
            "Sample Size": self.sample_size,
            "Demographics": self.demographics,
            "Reported Symptoms": self.reported_symptoms,
            "Transmission Routes": self.transmission_routes,
            "Vaccination Data": self.vaccination_data,
            "Outcomes": self.outcomes,
            "Study Methods": self.study_methods,
            "Key Findings": self.key_findings,
            "Risk Factors": self.risk_factors,
            "Recommendations": self.recommendations,
        }

    def __str__(self):
        """
        String representation of the data schema object.
        """
        return str(self.to_dict())


if __name__ == "__main__":

    paper = Paper(
        study_id="MPX2024-001",
        title="Epidemiological Insights into Mpox Outbreaks",
        authors=["Dr. A. Smith", "Dr. B. Jones"],
        publication_date="2024-12-01",
        journal="Global Health Journal",
        location="Sub-Saharan Africa",
        sample_size=1200,
        demographics={"age_range": "18-60", "gender_ratio": "60:40"},
        reported_symptoms=["fever", "rash", "lymphadenopathy"],
        transmission_routes=["close contact", "sexual contact"],
        vaccination_data={"coverage": 70, "efficacy": 85},
        outcomes={"recovered": 1150, "deceased": 50},
        study_methods="Retrospective cohort analysis",
        key_findings="High efficacy of vaccination in reducing severe outcomes.",
        risk_factors=["immunosuppression", "travel to endemic areas"],
        recommendations="Increase vaccination coverage and focus on vulnerable populations."
    )

    print(paper)
