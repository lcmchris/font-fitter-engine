from font_fitter_engine.loader import Loader
from font_fitter_engine.searcher import Searcher
from pathlib import Path


class SpacingEngine:
    def __init__(
        self,
        loader,
        searcher,
    ) -> None:
        self.loader: Loader = loader
        self.searcher: Searcher = searcher

    def run(self, path):
        path_b = Path(path)
        if not path_b.is_dir():
            raise NotImplementedError("Path should be a directory")
        for file in path_b.iterdir():
            print(f"Processing file {file}")
            self.loader.load(path=file)
            img_out = self.loader.process()
            calculated_spaces = self.searcher.search(img_out=img_out)
            print(calculated_spaces)
        print("Run complete")

    def validate(self, path: str):
        """
        Supply a path that is a directory or file.
        """
        path_b = Path(path)
        if not path_b.is_dir():
            raise NotImplementedError("Path should be a directory")

        validation_dict = {}
        for file in path_b.iterdir():
            filename = file.name
            self.loader.load(path=file)
            img_out = self.loader.process()
            spacing = self.loader.get_spacing()

            for glyph in self.loader.glyph_set:
                img = img_out[glyph].array
                height, width, c = img.shape
                glyph_spacing = spacing[glyph]
                lsb = glyph_spacing.lsb

                rsb = glyph_spacing.lsb
                center_x = width // 2
                sdf_array = self.searcher.transform.generate(img)
                x1 = center_x - lsb
                y1 = 0
                x2 = center_x
                y2 = height

                area = (x1, y1, x2, y2)
                for algo in self.searcher.algos:
                    calculated_darkness = algo.calculate(sdf_array, area)
                    if validation_dict.get(filename, None) is None:
                        validation_dict[filename] = {}

                    if validation_dict[filename].get(algo, None) is None:
                        validation_dict[filename][algo] = {}
                    if validation_dict[filename][algo].get(glyph, None) is None:
                        validation_dict[filename][algo][glyph] = {}

                    validation_dict[filename][algo][glyph]["calc_val"] = (
                        calculated_darkness
                    )
                    validation_dict[filename][algo][glyph]["lsb"] = lsb

        print(validation_dict)
        print("Validation complete")
