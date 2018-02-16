import os
import inspect
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# AlignCrop3DSlicerModule
#

class AlignCrop3DSlicerModule(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Align and Crop Volumes"
    self.parent.categories = ["Otolaryngology"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Eniolu (Auditory Biophyiscs Lab)"]
    self.parent.helpText = """
    This is a scripted loadable module.
    It aligns volumes to an ENT clinical reference and crops volumes based on
    a user provided template image
    """
    self.parent.acknowledgementText = """
    This process was developed at
    Western University(Ontario, CA) in the Auditory Biophyiscs Lab
""" # replace with organization, grant and thanks.

#
# AlignCrop3DSlicerModuleWidget
#
class AlignCrop3DSlicerModuleWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py"""

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        # Instantiate and connect widgets ...

        #
        # Align Volume Area
        #
        parametersCollapsibleButtonAlign = ctk.ctkCollapsibleButton()
        parametersCollapsibleButtonAlign.text = "Align Volume"
        self.layout.addWidget(parametersCollapsibleButtonAlign)

        # Layout within the Align collapsible button
        parametersFormLayoutAlign = qt.QFormLayout(parametersCollapsibleButtonAlign)

        #
        # Atlas Template selector
        #
        self.templateAtlasSelector = slicer.qMRMLNodeComboBox()
        self.templateAtlasSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.templateAtlasSelector.selectNodeUponCreation = True
        self.templateAtlasSelector.addEnabled = False
        self.templateAtlasSelector.removeEnabled = False
        self.templateAtlasSelector.noneEnabled = True
        self.templateAtlasSelector.showHidden = False
        self.templateAtlasSelector.showChildNodeTypes = False
        self.templateAtlasSelector.setMRMLScene( slicer.mrmlScene )
        self.templateAtlasSelector.setToolTip( "Pick the template image to register input volume to" )
        #
        #Atlas Fiducial template selector
        #
        self.templateFidSelector = slicer.qMRMLNodeComboBox()
        self.templateFidSelector.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.templateFidSelector.selectNodeUponCreation = True
        self.templateFidSelector.addEnabled = False
        self.templateFidSelector.removeEnabled = False
        self.templateFidSelector.noneEnabled = True
        self.templateFidSelector.showHidden = False
        self.templateFidSelector.showChildNodeTypes = False
        self.templateFidSelector.setMRMLScene( slicer.mrmlScene )
        self.templateFidSelector.setToolTip( "Pick template fiducials to register input volume fiducials to" )

        templateLayout = qt.QHBoxLayout()
        templateLayout.addWidget(self.templateAtlasSelector)
        templateLayout.addWidget(self.templateFidSelector)
        parametersFormLayoutAlign.addRow("Atlas Template & Fiducials: ", templateLayout)
        #
        # input volume selector
        #
        self.inputSelector = slicer.qMRMLNodeComboBox()
        self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputSelector.selectNodeUponCreation = True
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.noneEnabled = True
        self.inputSelector.showHidden = False
        self.inputSelector.showChildNodeTypes = False
        self.inputSelector.setMRMLScene( slicer.mrmlScene )
        self.inputSelector.setToolTip( "Pick the volume to align and/or Crop" )
        parametersFormLayoutAlign.addRow("Input Volume: ", self.inputSelector)

        #
        # Fiduical placement buttons
        #
        self.PAButton		 	= qt.QPushButton('Porus Acousticus')
        self.PAButton.toolTip 	= "Place porus acousticus fiducial"
        self.PAButton.enabled	= False

        self.GGButton		 	= qt.QPushButton('Geniculate Ganglion')
        self.GGButton.toolTip 	= "Place geniculate ganglion fiduical"
        self.GGButton.enabled	= False

        self.SFButton		 	= qt.QPushButton('Stylomastoid Formamen')
        self.SFButton.toolTip 	= "Place stylomastoid foramen fiducial"
        self.SFButton.enabled	= False

        self.AEButton			= qt.QPushButton('Arcuate Eminence')
        self.AEButton.toolTip 	= "Place arcuate eminence fiducial"
        self.AEButton.enabled	= False

        self.PSCButton			= qt.QPushButton('Posterior SC')
        self.PSCButton.toolTip 	= "Place posterior semicircular canal fiduical"
        self.PSCButton.enabled	= False

        self.OWButton		 	= qt.QPushButton('Oval Window')
        self.OWButton.toolTip 	= "Place oval window fiducial"
        self.OWButton.enabled	= False

        self.RWButton			= qt.QPushButton('Round Window')
        self.RWButton.toolTip 	= "Place round window fiducial"
        self.RWButton.enabled	= False

        fiduicalPlacement1 = qt.QHBoxLayout()
        fiduicalPlacement1.addWidget(self.PAButton)
        fiduicalPlacement1.addWidget(self.GGButton)
        fiduicalPlacement1.addWidget(self.SFButton)
        parametersFormLayoutAlign.addRow("Fiduical Placement: ", fiduicalPlacement1)

        fiduicalPlacement2 = qt.QHBoxLayout()
        fiduicalPlacement2.addWidget(self.AEButton)
        fiduicalPlacement2.addWidget(self.PSCButton)
        parametersFormLayoutAlign.addRow("Fiduical Placement: ", fiduicalPlacement2)

        fiduicalPlacement3 = qt.QHBoxLayout()
        fiduicalPlacement3.addWidget(self.OWButton)
        fiduicalPlacement3.addWidget(self.RWButton)
        parametersFormLayoutAlign.addRow("Fiduical Placement: ", fiduicalPlacement3)


        #
        # Align Button
        #
        self.alignButton = qt.QPushButton("Align")
        self.alignButton.toolTip = "Align volume to clinical reference"
        self.alignButton.enabled = False
        parametersFormLayoutAlign.addRow(self.alignButton)


        #
        #Crop Volume AREA
        #
        parametersCollapsibleButtonCrop = ctk.ctkCollapsibleButton()
        parametersCollapsibleButtonCrop.text = "Crop Volume"
        self.layout.addWidget(parametersCollapsibleButtonCrop)

        # Layout within the Crop collapsible button
        parametersFormLayoutCrop = qt.QFormLayout(parametersCollapsibleButtonCrop)

        #
        # input crop volume template selector
        #
        self.cropInputSelector = slicer.qMRMLNodeComboBox()
        self.cropInputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.cropInputSelector.selectNodeUponCreation = True
        self.cropInputSelector.addEnabled = True
        self.cropInputSelector.renameEnabled = True
        self.cropInputSelector.removeEnabled = True
        self.cropInputSelector.noneEnabled = True
        self.cropInputSelector.showHidden = False
        self.cropInputSelector.showChildNodeTypes = False
        self.cropInputSelector.setMRMLScene( slicer.mrmlScene )
        self.cropInputSelector.setToolTip( "select crop template volume " )
        parametersFormLayoutCrop.addRow("Crop Template Volume: ", self.cropInputSelector)


        #
        # output crop volume selector
        #
        self.cropOutputSelector = slicer.qMRMLNodeComboBox()
        self.cropOutputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.cropOutputSelector.selectNodeUponCreation = True
        self.cropOutputSelector.addEnabled = True
        self.cropOutputSelector.renameEnabled = True
        self.cropOutputSelector.removeEnabled = True
        self.cropOutputSelector.noneEnabled = True
        self.cropOutputSelector.showHidden = False
        self.cropOutputSelector.showChildNodeTypes = False
        self.cropOutputSelector.setMRMLScene( slicer.mrmlScene )
        self.cropOutputSelector.setToolTip( "Create new cropped volume " )
        parametersFormLayoutCrop.addRow("New Cropped Volume: ", self.cropOutputSelector)

        #
        #Define ROI & Crop buttons
        #
        self.defineCropButton		 	= qt.QPushButton('Define ROI')
        self.defineCropButton.toolTip 	= "define region of interest for cropping"
        self.defineCropButton.enabled	= False

        self.cropButton		 	        = qt.QPushButton('Crop!')
        self.cropButton.toolTip 	    = "define region of interest for cropping"
        self.cropButton.enabled	        = False

        imageCropping = qt.QHBoxLayout()
        imageCropping.addWidget(self.defineCropButton)
        imageCropping.addWidget(self.cropButton)
        parametersFormLayoutCrop.addRow("Select & Crop Region of Interest: ", imageCropping)

        #
        # Align Volume connections
        #
        self.templateAtlasSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlign)
        self.templateFidSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlign)
        self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlign)
        self.PAButton.connect('clicked(bool)', self.onPAButton)
        self.GGButton.connect('clicked(bool)', self.onGGButton)
        self.SFButton.connect('clicked(bool)', self.onSFButton)
        self.AEButton.connect('clicked(bool)', self.onAEButton)
        self.PSCButton.connect('clicked(bool)', self.onPSCButton)
        self.OWButton.connect('clicked(bool)', self.onOWButton)
        self.RWButton.connect('clicked(bool)', self.onRWButton)
        self.alignButton.connect('clicked(bool)', self.onAlignButton)
        self.cropInputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectCrop)
        self.cropOutputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectCrop)
        self.defineCropButton.connect('clicked(bool)', self.onDefineCropButton)
        self.cropButton.connect('clicked(bool)', self.onCropButton)

        # Add vertical spacer
        self.layout.addStretch(1)

        # Refresh select buttons' state
        self.onSelectAlign()
        self.onSelectCrop()

    def onPAButton(self):
        #Setup Fiduical placement
        self.movingFiducialNode = slicer.vtkMRMLMarkupsFiducialNode()
        slicer.mrmlScene.AddNode(self.movingFiducialNode)
        #Fiduical Placement Widget
        self.fiducialWidget = slicer.qSlicerMarkupsPlaceWidget()
        self.fiducialWidget.buttonsVisible = False
        self.fiducialWidget.placeButton().show()
        self.fiducialWidget.setMRMLScene(slicer.mrmlScene)
        self.fiducialWidget.setCurrentNode(self.movingFiducialNode)
        self.fiducialWidget.placeMultipleMarkups = slicer.qSlicerMarkupsPlaceWidget.ForcePlaceSingleMarkup

        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Porus Acousticus:\n\n" +
                                "Place fiducial on the centre of the porus acousticus.\n\n" +
                                "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.PAButton.enabled = False
        self.GGButton.enabled = True

    def onGGButton(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Geniculate Ganglion:\n\n" +
                                "Place fiduical on the geniculate ganglion.\n\n" +
                                "Press okay when ready" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.GGButton.enabled = False
        self.SFButton.enabled = True

    def onSFButton(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Stylomastoid Foramen:\n\n" +
                                "place fiducial at the point it becomes the canal.\n\n" +
                                "Press okay when ready" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.SFButton.enabled = False
        self.AEButton.enabled = True

    def onAEButton(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Arcuate Eminence:\n\n" +
                                "Place fiducial on the centre of the top of the superior semicircular canal.\n\n" +
                                "Press okay when ready" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.AEButton.enabled = False
        self.PSCButton.enabled = True

    def onPSCButton(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Posterior Semicircular Canal:\n\n" +
                                "Place fiduical on the mid point of the posterior semicircular canal.\n\n"
                                "Press okay when ready" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.PSCButton.enabled = False
        self.OWButton.enabled = True

    def onOWButton(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Oval Window:\n\n" +
                                "Place fiducial on the centre of the oval window.\n\n" +
                                "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.OWButton.enabled = False
        self.RWButton.enabled = True

    def onRWButton(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Round Window:\n\n" +
                                "Place fiduical on the centre of the round window.\n\n" +
                                "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)
        #Enable Alignment
        self.alignButton.enabled = True

    def onAlignButton(self):

        self.RWButton.enabled = False
        self.alignButton.enabled = False
        #TODO - logic for aligning images based on fiducials
        self.landmarkTransform = slicer.vtkMRMLTransformNode()
        slicer.mrmlScene.AddNode(self.landmarkTransform)

        logic = AlignCrop3DSlicerModuleLogic()
        if(self.movingFiducialNode.GetNumberOfFiducials() == 7):
            logic.runAlignmentRegistration(self.landmarkTransform, self.templateFid, self.movingFiducialNode)
        else:
            slicer.util.infoDisplay("7 Fiducials required for registration to proceed")

        #Apply Landmark transform on input Volume & Fiducials and Harden
        self.inputVolume.SetAndObserveTransformNodeID(self.landmarkTransform.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.inputVolume)
        self.movingFiducialNode.SetAndObserveTransformNodeID(self.landmarkTransform.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.movingFiducialNode)


        #TODO - Align output is incorrect!! Investigate (Jan 17th - 2018)

        #Set template to foreground in Slice Views
        applicationLogic 	= slicer.app.applicationLogic()
        selectionNode 		= applicationLogic.GetSelectionNode()
        selectionNode.SetSecondaryVolumeID(self.templateVolume.GetID())
        applicationLogic.PropagateForegroundVolumeSelection(0)

        #set overlap of foreground & background in slice view
        sliceLayout = slicer.app.layoutManager()
        sliceLogicR = sliceLayout.sliceWidget('Red').sliceLogic()
        compositeNodeR = sliceLogicR.GetSliceCompositeNode()
        compositeNodeR.SetForegroundOpacity(0.5)
        sliceLogicY = sliceLayout.sliceWidget('Yellow').sliceLogic()
        compositeNodeY = sliceLogicY.GetSliceCompositeNode()
        compositeNodeY.SetForegroundOpacity(0.5)
        sliceLogicG = sliceLayout.sliceWidget('Green').sliceLogic()
        compositeNodeG = sliceLogicG.GetSliceCompositeNode()
        compositeNodeG.SetForegroundOpacity(0.5)

    def onDefineCropButton(self):
        #TODO - develop process for automatically defining the region of interest
        slicer.app.layoutManager().setLayout(1) #Set to appropriate view (conventional)

        #Define Cropped Volume Parameters
        self.cropVolParamNode = slicer.vtkMRMLCropVolumeParametersNode()
        self.cropVolParamNode.SetScene(slicer.mrmlScene)
        self.cropVolParamNode.SetName('newCropVolume')
        self.cropVolParamNode.SetInputVolumeNodeID(self.cropTemplateVolume.GetID())
        self.cropVolParamNode.VoxelBasedOn()
        #logging.info(self.cropVolParamNode.GetVoxelBased())
        slicer.mrmlScene.AddNode(self.cropVolParamNode)

        #Fit ROI to input Volume and initialize in scene
        logic = AlignCrop3DSlicerModuleLogic()
        self.templateROI 	= slicer.vtkMRMLAnnotationROINode()
        self.templateROI.Initialize(slicer.mrmlScene)
        self.cropVolParamNode.SetROINodeID(self.templateROI.GetID())
        self.templateROI	= logic.runDefineCropROI(self.cropVolParamNode)

        #Enable cropping button
        self.cropButton.enabled = True

    def onCropButton(self):
        #TODO - Develop cropping process
        logic = AlignCrop3DSlicerModuleLogic()

        #cropVolume
        self.croppedVolume = logic.runCropVolume(   self.templateROI,
                                                    self.cropTemplateVolume)

    def cleanup(self):
        pass

    def onSelectAlign(self):
        self.PAButton.enabled =  self.templateAtlasSelector.currentNode() and self.templateFidSelector and self.inputSelector.currentNode()

        if(self.PAButton.enabled):
            self.inputVolume    = self.inputSelector.currentNode()
            self.templateVolume = self.templateAtlasSelector.currentNode()
            self.templateFid    = self.templateFidSelector.currentNode()

    def onSelectCrop(self):
        self.defineCropButton.enabled = self.cropInputSelector.currentNode() and self.cropOutputSelector.currentNode()

        if(self.defineCropButton.enabled):
            self.cropTemplateVolume = self.cropInputSelector.currentNode()


#
# AlignCrop3DSlicerModuleLogic
#

class AlignCrop3DSlicerModuleLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py"""

    def hasImageData(self,volumeNode):
        """This is an example logic method that
        returns true if the passed in volume
        node has valid image data
        """
        if not volumeNode:
          logging.debug('hasImageData failed: no volume node')
          return False
        if volumeNode.GetImageData() is None:
          logging.debug('hasImageData failed: no image data in volume node')
          return False
        return True

    def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
        """Validates if the output is not the same as input
        """
        if not inputVolumeNode:
          logging.debug('isValidInputOutputData failed: no input volume node defined')
          return False
        if not outputVolumeNode:
          logging.debug('isValidInputOutputData failed: no output volume node defined')
          return False
        if inputVolumeNode.GetID()==outputVolumeNode.GetID():
          logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
          return False
        return True

    def runAlignmentRegistration(self, transform, fixedFiducial, movingFiducial):
        #Retrieve fixed landmarks

        #TODO - load location of template fiducials
        #fiducialLocation    = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/ref_fid.fcsv'
        #fixedFiducialTuple  = slicer.util.loadMarkupsFiducialList(fiducialLocation, returnNode=True)
        #fixedFiducial       = fixedFiducialTuple[1] #Retrieve fiducial portion only

        #Setup and Run Landmark Registration
        cliParamsFidReg = {	'fixedLandmarks'	: fixedFiducial.GetID(),
		                    'movingLandmarks' 	: movingFiducial.GetID(),
		                    'ransformType' 	    : 'Rigid',
		                    'saveTransform' 	: transform.GetID() }

        cliRigTrans = slicer.cli.run( slicer.modules.fiducialregistration, None,
		                              cliParamsFidReg, wait_for_completion=True )

    def runDefineCropROI(self, cropParam):
        """
        defining region of interest for cropping purposes
        """
        vol 		= slicer.mrmlScene.GetNodeByID(cropParam.GetInputVolumeNodeID()	)
        volBounds	= [0,0,0,0,0,0]
        vol.GetRASBounds(volBounds)
        logging.info(volBounds)

        #Find Dimensions of Image
        volDim		= [  (volBounds[1]-volBounds[0]),
            			 (volBounds[3]-volBounds[2]),
            			 (volBounds[5]-volBounds[4])   ]
        roi			= slicer.mrmlScene.GetNodeByID(cropParam.GetROINodeID())

        #Find Center of Image
        volCenter 	= [  ((volBounds[0]+volBounds[1])/2),
            			 ((volBounds[2]+volBounds[3])/2),
                         ((volBounds[4]+volBounds[5])/2)   ]

        roi.SetXYZ(volCenter)
        roi.SetRadiusXYZ(volDim[0]/2, volDim[1]/2, volDim[2]/2 )
        return roi

    def runCropVolume(self, roi, volume):
        """"
        run volume Cropping
        """

        #cliParamCrop = {'':
        #                '':
        #                '':
        #               }

        logging.info('Cropping processing started')
        #Create Crop Volume Parameter node
        cropParamNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropParamNode.SetScene(slicer.mrmlScene)
        cropParamNode.SetName('Crop_volume_Node1')

        #Set volume and ROI required for cropping
        cropParamNode.SetInputVolumeNodeID(volume.GetID())
        cropParamNode.SetROINodeID(roi.GetID())
        cropParamNode.VoxelBasedOn()
        logging.info(cropParamNode.GetVoxelBased())
        slicer.mrmlScene.AddNode(cropParamNode)

        #Apply Cropping
        cropVolumeLogic = slicer.modules.cropvolume.logic()
        cropVolumeLogic.Apply(cropParamNode)
        cropVol = slicer.mrmlScene.GetNodeByID(cropParamNode.GetOutputVolumeNodeID())

        logging.info('Cropping processing completed')


        #TODO - needs to be voxel based! Perhapas consider using the slicer.cli.run(....) methodologies!!

        return cropVol


class AlignCrop3DSlicerModuleTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_AlignCrop3DSlicerModule1()

  def test_AlignCrop3DSlicerModule1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = AlignCrop3DSlicerModuleLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
