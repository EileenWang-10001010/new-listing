import argparse
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as trns
from PIL import Image

_GRAY = (218, 227, 218)
_GREEN = (18, 127, 15)
_WHITE = (255, 255, 255)

_COCO_INSTANCE_CATEGORY_NAMES = [
    "__background__", "person", "bicycle", "car", "motorcycle", "airplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant", "N/A", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "N/A", "backpack", "umbrella", "N/A", "N/A",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "N/A", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "couch", "potted plant", "bed", "N/A", "dining table",
    "N/A", "N/A", "toilet", "N/A", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "N/A", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]


def vis_bbox(image, bbox, color=_GREEN, thick=1):
    """Visualizes a bounding box."""
    image = image.astype(np.uint8)
    bbox = list(map(int, bbox))
    x0, y0, x1, y1 = bbox
    cv2.rectangle(image, (x0, y0), (x1, y1), color, thickness=thick)
    return image


def vis_mask(image, mask, col, alpha=0.4, show_border=True, border_thick=1):
    """Visualizes a single binary mask."""
    image = image.astype(np.float32)

    mask = mask >= 0.5
    mask = mask.astype(np.uint8)
    idx = np.nonzero(mask)

    image[idx[0], idx[1], :] *= 1.0 - alpha
    image[idx[0], idx[1], :] += alpha * col

    if show_border:
        contours = cv2.findContours(
            mask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)[-2]
        cv2.drawContours(image, contours, -1, _WHITE,
                         border_thick, cv2.LINE_AA)

    return image.astype(np.uint8)


def vis_class(image, bbox, text, bg_color=_GREEN, text_color=_GRAY, font_scale=0.35):
    """Visualizes the class."""
    image = image.astype(np.uint8)
    x0, y0 = int(bbox[0]), int(bbox[1])

    # Compute text size
    font = cv2.FONT_HERSHEY_SIMPLEX
    ((text_w, text_h), _) = cv2.getTextSize(text, font, font_scale, 1)

    # Place text background
    back_tl = x0, y0 - int(1.3 * text_h)
    back_br = x0 + text_w, y0
    cv2.rectangle(image, back_tl, back_br, bg_color, -1)

    # Show text
    text_tl = x0, y0 - int(0.3 * text_h)
    cv2.putText(image, text, text_tl, font, font_scale,
                text_color, lineType=cv2.LINE_AA)

    return image


def run_object_detection(model, image_path, transforms, threshold=0.5, output_path="out.png"):
    """Inference."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Read image and run prepro
    image = Image.open(image_path).convert("RGB")
    image_tensor = transforms(image)
    print(f"\n\nImage size after transformation: {image_tensor.size()}")

    # Feed input and get results at index 0
    # (input image is at index 0 in the list)
    outputs = model([image_tensor])[0]

    # Result postpro and vis
    display_image = np.array(image)
    outputs = {k: v.numpy() for k, v in outputs.items()}
    is_mask = True if "masks" in outputs else False
    if is_mask:
        outputs["masks"] = np.squeeze(outputs["masks"], axis=1)

    print("\n\nInference results:")
    for i, (bbox, label, score) in enumerate(zip(outputs["boxes"], outputs["labels"], outputs["scores"])):
        if score < threshold:
            continue

        print(
            f"Label {label}: {_COCO_INSTANCE_CATEGORY_NAMES[label]} ({score:.2f})")

        display_image = vis_bbox(display_image, bbox)
        display_image = vis_class(
            display_image, bbox, _COCO_INSTANCE_CATEGORY_NAMES[label])
        if is_mask:
            display_image = vis_mask(
                display_image, outputs["masks"][i], np.array([0., 0., 255.]))

    plt.figure(figsize=(10, 6))
    plt.imshow(display_image)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(output_path, bbox_inches="tight")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PyTorch Object Detection")
    parser.add_argument("--image_path", type=str,
                        default="images/sheep-herd-shepherd-hats-dog-meadow.jpg", help="path to image")
    parser.add_argument("--model_type", type=str,
                        default="fasterrcnn", help="fasterrcnn or maskrcnn")
    parser.add_argument("--output_path", type=str,
                        default="out.png", help="path to save output image")

    # Parse arguments
    args = parser.parse_args()

    # Define image transforms
    transforms = trns.ToTensor()

    # Load model
    if args.model_type == "fasterrcnn":
        model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    elif args.model_type == "maskrcnn":
        model = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    else:
        raise AssertionError

    print(model)

    # Set model to eval mode
    model.eval()

    # Run model
    with torch.no_grad():
        run_object_detection(model, args.image_path,
                             transforms, output_path=args.output_path)