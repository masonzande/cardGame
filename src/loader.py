import os

class ILoadable():
    def load_from_file(path: str) -> "ILoadable":
        raise Exception("Not Implemented")

class ContentLoader:
    content_root: str

    def __init__(self, root: str="assets"):
        self.content_root = root
    
    def load_custom[T: ILoadable](self, file_name: str, type: type[T]) -> T:
        file_location = os.path.join(self.content_root, file_name)
        if not os.path.exists(file_location):
            print(f"[ERR]: File {file_name} was not found.")
            raise FileNotFoundError()
        try:
            return type.load_from_file(file_location)
        except:
            print(f"[ERR]: Loading file {file_name} into type {type.__str__()} failed.")
            raise TypeError()
        