import os

def generate_file_path(file_id, file_name, content, file_type="img"):
    """
    Returns a string based on the the file type and name representing the path
    where the path is located

    Parameters
    ----------
    id: id of the file (int)
    file_type: type of the file (used to define the folder) (str)
    file_name: name of the file (str)
    content: supposed content of the file (str)

    Returns
    -------
    path: path to file storage (str)

    Note
    ----
    At this point, file_type should only be video or img

    Author: Antoine Mouchet
    """
    base = os.getcwd()
    
    # Chech to make sure there is something in content
    # Make sure that img and video were uploaded. Otherwise, it is useless to generate a path for them
    
    # if content not empty:
    return os.path.join(base, "app", "static", file_type, file_name, str(file_id))

    # else:
    # return ""