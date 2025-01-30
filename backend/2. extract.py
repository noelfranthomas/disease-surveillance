import os
import copy
import json
from collections import defaultdict
import pypdfium2 as pdfium  # Needs to be on top to avoid warnings

from surya.detection import batch_text_detection
from surya.input.load import load_from_file
from surya.input.pdflines import get_table_blocks
from surya.layout import batch_layout_detection
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.layout.model import load_model as load_layout_model
from surya.model.layout.processor import load_processor as load_layout_processor
from surya.model.table_rec.model import load_model
from surya.model.table_rec.processor import load_processor
from surya.tables import batch_table_recognition
from surya.postprocessing.heatmap import draw_bboxes_on_image
from surya.settings import settings
from surya.postprocessing.util import rescale_bbox

def process_pdf(input_path="example.pdf", results_dir="results"):
    model = load_model()
    processor = load_processor()

    layout_model = load_layout_model()
    layout_processor = load_layout_processor()

    det_model = load_det_model()
    det_processor = load_det_processor()

    # Load the PDF file
    images, _, _ = load_from_file(input_path)
    highres_images, names, text_lines = load_from_file(input_path, dpi=settings.IMAGE_DPI_HIGHRES, load_text_lines=True)
    folder_name = os.path.basename(input_path).split(".")[0]

    pnums = []
    prev_name = None
    for i, name in enumerate(names):
        if prev_name is None or prev_name != name:
            pnums.append(0)
        else:
            pnums.append(pnums[-1] + 1)

        prev_name = name

    layout_predictions = batch_layout_detection(images, layout_model, layout_processor)
    table_cells = []

    table_imgs = []
    table_counts = []

    for layout_pred, text_line, img, highres_img in zip(layout_predictions, text_lines, images, highres_images):
        # Detect tables in the layout
        bbox = [l.bbox for l in layout_pred.bboxes if l.label == "Table"]
        table_counts.append(len(bbox))

        if len(bbox) == 0:
            continue

        page_table_imgs = []
        highres_bbox = []
        for bb in bbox:
            highres_bb = rescale_bbox(bb, img.size, highres_img.size)
            page_table_imgs.append(highres_img.crop(highres_bb))
            highres_bbox.append(highres_bb)

        table_imgs.extend(page_table_imgs)

        # Detect table cells
        table_blocks = get_table_blocks(highres_bbox, text_line, highres_img.size) if text_line is not None else None
        if text_line is None or any(len(tb) == 0 for tb in table_blocks):
            det_results = batch_text_detection(page_table_imgs, det_model, det_processor)
            cell_bboxes = [[{"bbox": tb.bbox, "text": None} for tb in det_result.bboxes] for det_result in det_results]
            table_cells.extend(cell_bboxes)
        else:
            table_cells.extend(table_blocks)

    table_preds = batch_table_recognition(table_imgs, table_cells, model, processor)
    result_path = os.path.join(results_dir, folder_name)
    os.makedirs(result_path, exist_ok=True)

    table_predictions = defaultdict(list)
    for i, (pred, table_img) in enumerate(zip(table_preds, table_imgs)):
        orig_name = names[i]
        pnum = pnums[i]

        out_pred = pred.model_dump()
        out_pred["page"] = pnum + 1
        out_pred["table_idx"] = i
        table_predictions[orig_name].append(out_pred)

    # Save results to JSON
    with open(os.path.join(result_path, "results.json"), "w+", encoding="utf-8") as f:
        json.dump(table_predictions, f, ensure_ascii=False)

    print(f"Wrote results to {result_path}")

if __name__ == "__main__":
    process_pdf()
