import open_clip
import torch
from PIL import Image


class EmbeddingExtractor:

    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Using device: {self.device}")

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained="laion2b_s34b_b79k"
        )

        self.model.to(self.device)
        self.model.eval()

    def extract(self, image_path):

        """
        Extract a normalized CLIP embedding from an image.

        Parameters
        ----------
        image_path : str
            Path to the image.

        Returns
        -------
        numpy.ndarray
            512-dimensional normalized embedding.
        """

        try:

            image = Image.open(image_path).convert("RGB")

        except Exception as e:

            raise RuntimeError(
                f"Unable to open image: {image_path}\n{e}"
            )

        image = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():

            embedding = self.model.encode_image(image)

            # Normalize embedding (Cosine Similarity)
            embedding = embedding / embedding.norm(
                dim=-1,
                keepdim=True
            )

        return embedding.cpu().numpy().flatten()