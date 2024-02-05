import meshio
import numpy as np

def BBoxAnalysis(meshPath):
    mesh = meshio.read(meshPath)
    nodes = mesh.points
    x_values = nodes[:, 0]
    y_values = nodes[:, 1]
    z_values = nodes[:, 2]
    bbox = (np.min(x_values), np.max(x_values), np.max(y_values), np.min(y_values), np.max(z_values), np.min(z_values))
    return bbox

def GetNodesIDAtSection(mesh, section_value, axis):
    """
    :param mesh: obj from meshio.read
    :param section_value: value to evaluate
    :param axis: x = 0; y = 1; z = 2
    :return: np array nodes ID
    """
    nodes = mesh.points
    tol = 0.1
    listID = []
    for i in range(nodes.shape[0]):
        cur = nodes[i, axis]
        if (cur >= section_value - tol) and (cur <= section_value +tol) :
            listID.append(i)
    # to write into .txt
    # np.savetxt(path_to_file, np.asarray(listID),fmt="%i")
    return np.asarray(listID)

def GetNodesAtBoundary(meshPath, bbox, up_or_down):
    """
    :param mesh: PATH
    :param bbox: tuple
    :return:list

    UP = 1
    DOWN = 0
    """
    mesh = meshio.read(meshPath)
    x_values = bbox[0:2]
    y_values = bbox[2:4]
    z_values = bbox[4:6]
    # c1 = np.array([x_values[0], y_values[0], z_values[0]])
    # c2 = np.array([x_values[1], y_values[0], z_values[0]])
    c3 = np.array([x_values[0], y_values[up_or_down], z_values[0]])
    c4 = np.array([x_values[1], y_values[up_or_down], z_values[0]])
    # c5 = np.array([x_values[0], y_values[0], z_values[1]])
    # c6 = np.array([x_values[1], y_values[0], z_values[1]])
    c7 = np.array([x_values[0], y_values[up_or_down], z_values[1]])
    c8 = np.array([x_values[1], y_values[up_or_down], z_values[1]])
    corners = [c3,c4,c7,c8]
    listID = []
    for i in corners:
        condition = np.all(mesh.points == i, axis=1)
        index = np.where(condition)[0][0]
        listID.append(index)
    return listID