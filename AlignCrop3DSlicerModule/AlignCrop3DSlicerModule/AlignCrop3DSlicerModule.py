import os
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
    It aligns volumes to an ENT clinical reference and crops volumes
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
        self.templateSelector = slicer.qMRMLNodeComboBox()
        self.templateSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.templateSelector.selectNodeUponCreation = True
        self.templateSelector.addEnabled = False
        self.templateSelector.removeEnabled = False
        self.templateSelector.noneEnabled = False
        self.templateSelector.showHidden = False
        self.templateSelector.showChildNodeTypes = False
        self.templateSelector.setMRMLScene( slicer.mrmlScene )
        self.templateSelector.setToolTip( "Pick the template to register input volume to" )
        parametersFormLayoutAlign.addRow("Atlas Template: ", self.templateSelector)

        #
        # input volume selector
        #
        self.inputSelector = slicer.qMRMLNodeComboBox()
        self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputSelector.selectNodeUponCreation = True
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.noneEnabled = False
        self.inputSelector.showHidden = False
        self.inputSelector.showChildNodeTypes = False
        self.inputSelector.setMRMLScene( slicer.mrmlScene )
        self.inputSelector.setToolTip( "Pick the volume to align and/or Crop" )
        parametersFormLayoutAlign.addRow("Input Volume: ", self.inputSelector)

        #
        # Fiduical placement buttons
        #
        self.button1		 	= qt.QPushButton('Fiduical 1')
        self.button1.toolTip 	= "Place first fiduical"
        self.button1.enabled	= False

        self.button2			=qt.QPushButton('Fiduical 2')
        self.button2.toolTip 	= "Place second fiduical"
        self.button2.enabled	= False

        self.button3		 	= qt.QPushButton('Fiducial 3')
        self.button3.toolTip 	= "Place third fiduical"
        self.button3.enabled	= False

        self.button4			= qt.QPushButton('Fiduical 4')
        self.button4.toolTip 	= "Place fourth fiduical"
        self.button4.enabled	= False

        fiduicalPlacement = qt.QHBoxLayout()
        fiduicalPlacement.addWidget(self.button1)
        fiduicalPlacement.addWidget(self.button2)
        fiduicalPlacement.addWidget(self.button3)
        fiduicalPlacement.addWidget(self.button4)
        parametersFormLayoutAlign.addRow("Fiduical Placement: ", fiduicalPlacement)

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
        # output crop volume selector
        #
        self.outputSelector = slicer.qMRMLNodeComboBox()
        self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.outputSelector.selectNodeUponCreation = True
        self.outputSelector.addEnabled = True
        self.outputSelector.renameEnabled = True
        self.outputSelector.removeEnabled = True
        self.outputSelector.noneEnabled = True
        self.outputSelector.showHidden = False
        self.outputSelector.showChildNodeTypes = False
        self.outputSelector.setMRMLScene( slicer.mrmlScene )
        self.outputSelector.setToolTip( "Create new cropped volume " )
        parametersFormLayoutCrop.addRow("New Cropped Volume: ", self.outputSelector)

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
        self.templateSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.button1.connect('clicked(bool)', self.onButton1)
        self.button2.connect('clicked(bool)', self.onButton2)
        self.button3.connect('clicked(bool)', self.onButton3)
        self.button4.connect('clicked(bool)', self.onButton4)
        self.alignButton.connect('clicked(bool)', self.onAlignButton)
        self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect2)
        self.defineCropButton.connect('clicked(bool)', self.onDefineCropButton)
        self.cropButton.connect('clicked(bool)', self.onCropButton)


        # Add vertical spacer
        self.layout.addStretch(1)

        # Refresh Apply button state
        self.onSelect()

        self.onSelect2()

    def onButton1(self):
        #Setup Fiduical placement
        self.movingFiducialNode = slicer.vtkMRMLMarkupsFiducialNode()
        slicer.mrmlScene.AddNode(self.movingFiducialNode)
        #Fiduical Placement Widget
        self.fiducialWidget = slicer.qSlicerMarkupsPlaceWidget()
        self.fiducialWidget.buttonsVisible = False
        self.fiducialWidget.placeButton().show()
        self.fiducialWidget.setMRMLScene(slicer.mrmlScene)
        self.fiducialWidget.setCurrentNode(self.templateSelector.currentNode())
        self.fiducialWidget.placeMultipleMarkups = slicer.qSlicerMarkupsPlaceWidget.ForcePlaceSingleMarkup

        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Place corresponding fiducial 1:\n\n" +
                                "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.button1.enabled = False
        self.button2.enabled = True

    def onButton2(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Place corresponding fiducial 2:\n\n" +
                                    "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.button2.enabled = False
        self.button3.enabled = True

    def onButton3(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Place corresponding fiducial 3:\n\n" +
                                    "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)

        self.button3.enabled = False
        self.button4.enabled = True

    def onButton4(self):
        #Delay to ensure Widget Appears & provide user with info
        slicer.util.infoDisplay("Place corresponding fiducial 4:\n\n" +
                                    "Press okay when ready to begin" )

        #Enable fiducial placement
        self.fiducialWidget.setPlaceModeEnabled(True)
        #Enable Alignment
        self.alignButton.enabled = True

    def onAlignButton(self):

        self.button4.enabled = False
        #TODO - logic for aligning images based on fiducials
        self.landmarkTransform = slicer.vtkMRMLTransformNode()
        slicer.mrmlScene.AddNode(self.LandmarkTrans)

        logic = AlignCrop3DSlicerModuleLogic()
        if(self.placedLandmarkNode.GetNumberOfFiducials() == 4):
            logic.runAlignmentRegistration(self.landmarkTransform, self.movingFiducialNode)
        else:
            slicer.util.infoDisplay("4 Fiducials required for registration to proceed")

        #Apply Landmark transform on input Volume and Harden
        self.inputVolume.SetAndObserveTransformNodeID(self.landmarkTransform.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.inputVolume)

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
        self.cropVolParamNode.SetInputVolumeNodeID(self.templateVolume.GetID())
        self.cropVolParamNode.VoxelBasedOn()
        #logging.info(self.cropVolParamNode.GetVoxelBased())
        slicer.mrmlScene.AddNode(self.cropVolParamNode)

        #Fit ROI to input Volume and initialize in scene
        logic = AValue3DSlicerModuleLogic()
        self.atlasROI 		= slicer.vtkMRMLAnnotationROINode()
        self.atlasROI.Initialize(slicer.mrmlScene)
        self.cropVolumeNode.SetROINodeID(self.atlasROI.GetID())
        self.atlasROI	= logic.runDefineCropROI(self.cropVolParamNode)

    def onCropButton(self):
        #TODO - Develop cropping process
        logic = AValue3DSlicerModuleLogic()

    def cleanup(self):
        pass

    def onSelect(self):
        self.button1.enabled = self.templateSelector.currentNode() and self.inputSelector.currentNode()

        if(self.button1.enabled):
            self.inputVolume    = self.inputSelector.currentNode()
            self.templateVolume = self.templateSelector.currentNode()

    def onSelect2(self):
        if self.outputSelector.currentNode():
            self.defineCropButton.enabled = true


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

    def runAlignmentRegistration(self, transform, movingFiducial):
        #Retrieve fixed landmarks
        #TODO - load location of template fiducials
        fiducialLocation = "User Specified fiducial location"
        fixedFiducial = slicer.util.loadMarkupsFiducialList(fiducialLocation, returnNode=True)

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
        logging.info('Cropping processing started')
        #Create Crop Volume Parameter node
        cropParamNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropParamNode.SetScene(slicer.mrmlScene)
        cropParamNode.SetName('Crop_volume_Node1')

        #Set volume and ROI required for cropping
        cropParamNode.SetInputVolumeNodeID(volume.GetID())
        cropParamNode.SetROINodeID(roi.GetID())
        cropParamNode.VoxelBasedOff()
        logging.info(cropParamNode.GetVoxelBased())
        slicer.mrmlScene.AddNode(cropParamNode)

        #Apply Cropping
        cropVolumeLogic = slicer.modules.cropvolume.logic()
        cropVolumeLogic.Apply(cropParamNode)
        cropVol = slicer.mrmlScene.GetNodeByID(cropParamNode.GetOutputVolumeNodeID())

        logging.info('Cropping processing completed')

        return cropVol

    def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
        """
        Run the actual algorithm
        """

        if not self.isValidInputOutputData(inputVolume, outputVolume):
            slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
            return False

        logging.info('Processing started')

        # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
        cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
        cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

        # Capture screenshot
        if enableScreenshots:
            self.takeScreenshot('AlignCrop3DSlicerModuleTest-Start','MyScreenshot',-1)

        logging.info('Processing completed')
        return True


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
