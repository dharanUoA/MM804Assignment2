import vtk

# Specify the path to your DICOM files
dicom_directory = "CT"

# Create a DICOM reader
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dicom_directory)
reader.Update()

# # Get information about the DICOM dataset
# dimension = reader.GetOutput().GetDimensions()
# voxel_resolution = reader.GetOutput().GetSpacing()
# data_range = reader.GetOutput().GetScalarRange()

# # Display the obtained information
# print("Dimension:", dimension)
# print("Voxel Resolution:", voxel_resolution)
# print("Minimum Pixel Intensity:", data_range[0])
# print("Maximum Pixel Intensity:", data_range[1])

# Create a volume property
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.ShadeOn()
# volumeProperty.SetInterpolationTypeToLinear()

# Create a color transfer function
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(-1024, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(-512, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0, 0, 0, 0)
colorTransferFunction.AddRGBPoint(100, 1.0, 0.8, 0.6)  # Soft tissues in brown
colorTransferFunction.AddRGBPoint(500, 1.0, 1.0, 1.0)  # Bones in white

# Create an opacity transfer function
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(-1024, 0.0)
opacityTransferFunction.AddPoint(-512, 0.0)
opacityTransferFunction.AddPoint(0, 0.0)
opacityTransferFunction.AddPoint(100, 0.2) # Soft tissues
opacityTransferFunction.AddPoint(500, 0.8)  # Bones

# Set the transfer functions in the volume property
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)

# Create a volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Create a volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# iso surface using marching cube algorithm
isoSurface = vtk.vtkMarchingCubes()
isoSurface.SetInputConnection(reader.GetOutputPort())
isoSurface.SetValue(0, 200)

# Create a mapper for the iso-surface
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(isoSurface.GetOutputPort())

# Create an actor for the iso-surface
isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)

# Create a renderer and render window
renderer1 = vtk.vtkRenderer()
renderer1.AddVolume(volume)
renderer1.SetBackground(1.0, 1.0, 1.0) 
renderer1.SetViewport(0.0, 0.0, 0.33, 1.0)

renderer2 = vtk.vtkRenderer()
renderer2.AddActor(isoActor)
renderer2.SetBackground(1.0, 1.0, 1.0) 
renderer2.SetViewport(0.33, 0.0, 0.66, 1.0)

renderer3 = vtk.vtkRenderer()
renderer3.AddVolume(volume)
renderer3.AddActor(isoActor)
renderer3.SetBackground(1.0, 1.0, 1.0) 
renderer3.SetViewport(0.66, 0.0, 1.0, 1.0)

renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(1650, 550)
renderWindow.AddRenderer(renderer1)
renderWindow.AddRenderer(renderer2)
renderWindow.AddRenderer(renderer3)

# Set up a render window interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# sync all renderer cameras
camera = renderer1.GetActiveCamera()
renderer2.SetActiveCamera(camera)
renderer3.SetActiveCamera(camera)

renderer1.ResetCamera()
renderer2.ResetCamera()
renderer3.ResetCamera()

# Start the rendering loop
renderWindow.Render()
renderWindowInteractor.Start()
