import sys
sys.path.append(r"C:\Users\Veronica\sofa\v22.06.00\plugins\SofaPython3\lib\python3\site-packages")
import Sofa.Simulation, Sofa.Gui, Sofa.Core, SofaRuntime
import KeyPressedController
import os
import numpy as np

datapath = r"C:\Users\Veronica\Desktop\PhD\FuTURO\mesh\2CONNECTEDLAYERS"

# == ANATOMY FILES
l1 = "anatomy"
l2 = "muscle"
# mechanical mesh
l1mechpath = os.path.join(datapath, l1, f"{l1}.msh")
l2mechpath = os.path.join(datapath, l2, f"{l2}.msh")
# constraint
l1FixedPath = os.path.join(datapath, l1, "fixedID.txt")
l1FixedNodes = np.loadtxt(l1FixedPath, dtype=int)
l1Edge1 = np.loadtxt(os.path.join(datapath, l1, "edge1.txt"), dtype=int)
l1Edge2 = np.loadtxt(os.path.join(datapath, l1, "edge2.txt"), dtype=int)
l1Edge3 = np.loadtxt(os.path.join(datapath, l1, "edge3.txt"), dtype=int)
l1Edge4 = np.loadtxt(os.path.join(datapath, l1, "edge4.txt"), dtype=int)
l1InterfacePath = os.path.join(datapath, l1, "interfaceID.txt")
l1InterfaceNodes = np.loadtxt(l1InterfacePath, dtype=int)
l2InterfacePath = os.path.join(datapath, l2, "interfaceID.txt")
l2InterfaceNodes = np.loadtxt(l2InterfacePath, dtype=int)
# collision mesh
l2collpath= os.path.join(datapath, l2, f"{l2}-collision-up.stl") # collision only to detect interaction with the instrument
# visual mesh
platepath = r"C:\Users\Veronica\Desktop\PhD\FuTURO\mesh\2CONNECTEDLAYERS\visual\plate.obj"
visualanatomypath = r"C:\Users\Veronica\Desktop\PhD\FuTURO\mesh\2CONNECTEDLAYERS\visual\visual-skin.stl"
visualvesselpath = r"C:\Users\Veronica\Desktop\PhD\FuTURO\mesh\2CONNECTEDLAYERS\visual\visual-vessel.obj"

# == TOOL FILES
telemedPath = os.path.join(datapath, "tool", "Telemed_remeshed.stl" )
soundSafePath = os.path.join(datapath, "tool", "transducteur_annulaire.STL" )

def createScene(root):
    root.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels hideCollisionModels hideMappings showForceFields ')
    root.addObject('FreeMotionAnimationLoop')
    root.addObject('DefaultVisualManagerLoop')
    root.addObject('GenericConstraintSolver', tolerance='1e-9', maxIt='1000')
    root.addObject('DefaultPipeline', draw='0', depth='6', verbose='1')
    root.addObject('BruteForceBroadPhase', name='N2')
    root.addObject('BVHNarrowPhase')
    # root.addObject('RayTraceNarrowPhase')
    # root.addObject("NewProximityIntersection", name="Proximity", alarmDistance="2", contactDistance="0.7")
    root.addObject('LocalMinDistance', contactDistance='1.2', alarmDistance='1.8', name='localmindistance')

    root.addObject('DefaultContactManager', name='Response', response='FrictionContactConstraint')

    # ====== ASSEMBLY ======
    assembly = root.addChild("assembly")
    # assembly.addObject('EulerImplicitSolver', rayleighStiffness="0.1", rayleighMass="0.1")
    # assembly.addObject('SparseLDLSolver', name='l1Solver', template="CompressedRowSparseMatrixMat3x3d")
    # ====== FIRST LAYER ====
    anatomy = assembly.addChild("anatomy")
    anatomy.addObject('MeshGmshLoader', name="AnatomyMesh", filename=l1mechpath, rotation="0 0 180" )
    anatomy.addObject('EulerImplicitSolver', rayleighStiffness="0.1", rayleighMass="0.1")
    anatomy.addObject('SparseLDLSolver', name='l1Solver', template="CompressedRowSparseMatrixMat3x3d")
    anatomy.addObject('TetrahedronSetTopologyContainer', name="l1topology", src="@AnatomyMesh")
    anatomy.addObject('TetrahedronSetTopologyModifier', name='TopoModi')
    anatomy.addObject('TetrahedronSetGeometryAlgorithms', name="geomAlgo", template="Vec3d")
    anatomy.addObject('MechanicalObject', name="l1dofs", template="Vec3d"),
    anatomy.addObject('MeshMatrixMass', totalMass="3.567e-4", topology='@l1topology')
    anatomy.addObject('TetrahedralCorotationalFEMForceField', name='CFEM', youngModulus=3, poissonRatio=0.4, method="large")
    anatomy.addObject('FixedConstraint', name="lower", indices=l1FixedNodes)
    # anatomy.addObject('FixedConstraint', name="edge1",indices=l1Edge1)
    # anatomy.addObject('FixedConstraint', name="edge2",indices=l1Edge2)
    # anatomy.addObject('FixedConstraint', name="edge3", indices=l1Edge3)
    # anatomy.addObject('FixedConstraint', name="edge4", indices=l1Edge4)

    # collision = anatomy.addChild("l1collision")
    # collision.addObject('MeshSTLLoader', name='Loader', filename=l1collpath, flipNormals=0, rotation="0 0 180") #
    # collision.addObject('MeshTopology', src='@Loader')
    # collision.addObject('MechanicalObject', src='@Loader', name='l1collisDofs')
    # collision.addObject('TriangleCollisionModel')
    # collision.addObject('PointCollisionModel')
    # collision.addObject('LineCollisionModel')
    # collision.addObject('BarycentricMapping', input='@../l1dofs', output='@l1collisDofs')
    vesselVisual = anatomy.addChild("anatomyVisual")
    loaderVV = vesselVisual.addObject("MeshOBJLoader", name='Loader', filename=visualvesselpath, flipNormals=0, rotation="0 0 180")
    vesselVisual.addObject('OglModel', name="visu", src=loaderVV.getLinkPath(), color=[1.,0.,0.,0.5])
    vesselVisual.addObject('BarycentricMapping', name="BM", input='@../l1dofs', output='@visu')

    anatomy.addObject("LinearSolverConstraintCorrection")

    # ====== SECOND LAYER ======
    muscle = assembly.addChild("muscle")
    muscle.addObject('MeshGmshLoader', name="AnatomyMesh", filename=l2mechpath, rotation="0 0 180") #
    muscle.addObject('EulerImplicitSolver', rayleighStiffness="0.1", rayleighMass="0.1")
    muscle.addObject('SparseLDLSolver', name='l2Solver', template="CompressedRowSparseMatrixMat3x3d")
    muscle.addObject('TetrahedronSetTopologyContainer', name="l2topology", src="@AnatomyMesh")
    muscle.addObject('TetrahedronSetTopologyModifier', name='TopoModi')
    muscle.addObject('TetrahedronSetGeometryAlgorithms', name="geomAlgo", template="Vec3d")
    muscle.addObject('MechanicalObject', name="l2dofs", template="Vec3d"),
    muscle.addObject('MeshMatrixMass', totalMass="1.17e-4", topology='@l2topology')
    muscle.addObject('TetrahedralCorotationalFEMForceField', name='CFEM', youngModulus=2, poissonRatio=0.4, method="large")


    collisionUP = muscle.addChild("l2collisionUP")
    collisionUP.addObject('MeshSTLLoader', name='Loader', filename=l2collpath, flipNormals=0,  rotation="0 0 180")
    collisionUP.addObject('MeshTopology', src='@Loader')
    collisionUP.addObject('MechanicalObject', src='@Loader', name='l2collisDofsUP')
    collisionUP.addObject('TriangleCollisionModel')
    collisionUP.addObject('PointCollisionModel')
    collisionUP.addObject('LineCollisionModel')
    collisionUP.addObject('BarycentricMapping', input='@../l2dofs', output='@l2collisDofsUP')

    # visualSkin = muscle.addChild("anatomyVisual")
    # skinl=visualSkin.addObject('MeshSTLLoader', name='skinLoader', filename=visualanatomypath, flipNormals=0, rotation="0 0 180")
    # visualSkin.addObject('OglModel', name="skinVisu", src=skinl.getLinkPath(), color=[0.5,0.5,0.,0.5])
    # visualSkin.addObject('BarycentricMapping', name="BM", input='@../l2dofs', output='@skinVisu')

    muscle.addObject("LinearSolverConstraintCorrection")

    assembly.addObject("AttachConstraint", object1="@anatomy", object2="@muscle", twoWay="true", indices1=l1InterfaceNodes, indices2 = l2InterfaceNodes, constraintFactor=[1 for i in range(40)])


    # === TOOL
    tool = root.addChild("tool")
    loader = tool.addObject("MeshSTLLoader", name = "toolLoader", filename = telemedPath, rotation="0 0 180", translation="30 0 0")
    tool.addObject('MeshTopology', src='@toolLoader')
    tooldofs = tool.addObject("MechanicalObject", name="tooldofs", src="@toolLoader")
    # te = tool.addObject("TransformEngine", name="te", input_position=tooldofs.position.getLinkPath(), rotation=[0, 0, 0])
    tool.addObject('TriangleCollisionModel')
    tool.addObject('PointCollisionModel')
    tool.addObject('LineCollisionModel')

    visu = tool.addChild("toolVisual")
    visu.addObject('OglModel', name="visu", src=loader.getLinkPath())
    visu.addObject('IdentityMapping', name="IM", src=tooldofs.getLinkPath())

    # === PLATE
    plate = root.addChild("plate")
    plateloader = plate.addObject("MeshOBJLoader", name = "plateLoader", filename = platepath, rotation="0 0 180")
    plate.addObject('MeshTopology', src='@plateLoader')
    platemo = plate.addObject("MechanicalObject", name="platedofs", src="@plateLoader")
    visu = plate.addChild("plateVisual")
    visu.addObject('OglModel', name="visu", src=plateloader.getLinkPath())
    visu.addObject('IdentityMapping', name="IM", src=platemo.getLinkPath())

    root.addObject(KeyPressedController.RotationController(tool = root.tool))



if __name__ == '__main__':
    USE_GUI = True
    plugins = ["SofaComponentAll", "Sofa.Component.AnimationLoop", "Sofa.Component.Collision.Detection.Algorithm",
               'Sofa.Component.Collision.Detection.Intersection', 'Sofa.Component.IO.Mesh',
               'Sofa.Component.SolidMechanics.FEM.Elastic', 'Sofa.Component.LinearSolver.Direct',
               'Sofa.GL.Component.Rendering3D', "Sofa.Component.Engine.Select"]
    for p in plugins:
        SofaRuntime.importPlugin(p)
    # Create the root node
    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        # Execute simulation in background, without GUI
        for iteration in range(100000):
            Sofa.Simulation.animate(root, root.dt.value)
            print(f"Iteration: {iteration}")

    else:
        # Find out the supported GUIs
        print("Supported GUIs are: " + Sofa.Gui.GUIManager.ListSupportedGUI(","))
        # Launch the GUI (qt or qglviewer)
        Sofa.Gui.GUIManager.Init("myscene" , "qglviewer")
        Sofa.Gui.GUIManager.createGUI(root , __file__)
        Sofa.Gui.GUIManager.SetDimension(1080 , 1080)

        # Initialization of the scene will be done here
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()

        print("GUI was closed")

    print("Simulation is done.")