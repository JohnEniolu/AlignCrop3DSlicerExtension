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
        # Align Volume Area Cochlear Only (CO)
        #
        parametersCollapsibleButtonAlignCO = ctk.ctkCollapsibleButton()
        parametersCollapsibleButtonAlignCO.text = "Align Volume (Cochlea Only)"
        self.layout.addWidget(parametersCollapsibleButtonAlignCO)

        # Layout within the Align collapsible button
        parametersFormLayoutAlignCO = qt.QFormLayout(parametersCollapsibleButtonAlignCO)

        #
        # Atlas Template selector
        #
        self.templateAtlasSelectorCO = slicer.qMRMLNodeComboBox()
        self.templateAtlasSelectorCO.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.templateAtlasSelectorCO.selectNodeUponCreation = True
        self.templateAtlasSelectorCO.addEnabled = False
        self.templateAtlasSelectorCO.removeEnabled = False
        self.templateAtlasSelectorCO.noneEnabled = True
        self.templateAtlasSelectorCO.showHidden = False
        self.templateAtlasSelectorCO.showChildNodeTypes = False
        self.templateAtlasSelectorCO.setMRMLScene( slicer.mrmlScene )
        self.templateAtlasSelectorCO.setToolTip( "Pick the template image to register input volume to" )
        #
        #Atlas Fiducial template selector
        #
        self.templateFidSelectorCO = slicer.qMRMLNodeComboBox()
        self.templateFidSelectorCO.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.templateFidSelectorCO.selectNodeUponCreation = True
        self.templateFidSelectorCO.addEnabled = False
        self.templateFidSelectorCO.removeEnabled = False
        self.templateFidSelectorCO.noneEnabled = True
        self.templateFidSelectorCO.showHidden = False
        self.templateFidSelectorCO.showChildNodeTypes = False
        self.templateFidSelectorCO.setMRMLScene( slicer.mrmlScene )
        self.templateFidSelectorCO.setToolTip( "Pick template fiducials to register input volume fiducials to" )

        templateLayoutCO = qt.QHBoxLayout()
        templateLayoutCO.addWidget(self.templateAtlasSelectorCO)
        templateLayoutCO.addWidget(self.templateFidSelectorCO)
        parametersFormLayoutAlignCO.addRow("Atlas Template & Fiducials: ", templateLayoutCO)
        #
        # input volume selector
        #
        self.inputSelectorCO = slicer.qMRMLNodeComboBox()
        self.inputSelectorCO.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputSelectorCO.selectNodeUponCreation = True
        self.inputSelectorCO.addEnabled = False
        self.inputSelectorCO.removeEnabled = False
        self.inputSelectorCO.noneEnabled = True
        self.inputSelectorCO.showHidden = False
        self.inputSelectorCO.showChildNodeTypes = False
        self.inputSelectorCO.setMRMLScene( slicer.mrmlScene )
        self.inputSelectorCO.setToolTip( "Pick the volume to align " )
        parametersFormLayoutAlignCO.addRow("Align Input Volume: ", self.inputSelectorCO)


        #
        # Fiduical buttons for Inner Ear (Cochlea) Only registration
        #
        self.OWButtonCO		 	= qt.QPushButton("Oval Window")
        self.OWButtonCO.toolTip = "Place Oval Window Fiduical"
        self.OWButtonCO.enabled	= False

        self.CNButton			= qt.QPushButton('Cochlear Nerve')
        self.CNButton.toolTip 	= "Place Cochlear Nerve Fiduical"
        self.CNButton.enabled	= False

        self.AButton		 	= qt.QPushButton("Apex")
        self.AButton.toolTip 	= "Place Apex Fiduical"
        self.AButton.enabled	= False

        self.RWButtonCO			= qt.QPushButton('Round Window')
        self.RWButtonCO.toolTip = "Place Round Window Fiduical"
        self.RWButtonCO.enabled	= False

        fiduicalPlacementCO = qt.QHBoxLayout()
        fiduicalPlacementCO.addWidget(self.OWButtonCO)
        fiduicalPlacementCO.addWidget(self.CNButton)
        fiduicalPlacementCO.addWidget(self.AButton)
        fiduicalPlacementCO.addWidget(self.RWButtonCO)
        parametersFormLayoutAlignCO.addRow("Fiduical Placement: ", fiduicalPlacementCO)

        #
        # Align Button
        #
        self.alignButtonCO = qt.QPushButton("Align")
        self.alignButtonCO.toolTip = "Align volume to clinical reference"
        self.alignButtonCO.enabled = False
        parametersFormLayoutAlignCO.addRow(self.alignButtonCO)


        #
        # Align Volume Area (Temporal Bone)
        #
        parametersCollapsibleButtonAlignTB = ctk.ctkCollapsibleButton()
        parametersCollapsibleButtonAlignTB.text = "Align Volume (Temporal Bone)"
        self.layout.addWidget(parametersCollapsibleButtonAlignTB)

        # Layout within the Align collapsible button
        parametersFormLayoutAlignTB = qt.QFormLayout(parametersCollapsibleButtonAlignTB)

        #
        # Atlas Template selector
        #
        self.templateAtlasSelectorTB = slicer.qMRMLNodeComboBox()
        self.templateAtlasSelectorTB.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.templateAtlasSelectorTB.selectNodeUponCreation = True
        self.templateAtlasSelectorTB.addEnabled = False
        self.templateAtlasSelectorTB.removeEnabled = False
        self.templateAtlasSelectorTB.noneEnabled = True
        self.templateAtlasSelectorTB.showHidden = False
        self.templateAtlasSelectorTB.showChildNodeTypes = False
        self.templateAtlasSelectorTB.setMRMLScene( slicer.mrmlScene )
        self.templateAtlasSelectorTB.setToolTip( "Pick the template image to register input volume to" )
        #
        #Atlas Fiducial template selector
        #
        self.templateFidSelectorTB = slicer.qMRMLNodeComboBox()
        self.templateFidSelectorTB.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
        self.templateFidSelectorTB.selectNodeUponCreation = True
        self.templateFidSelectorTB.addEnabled = False
        self.templateFidSelectorTB.removeEnabled = False
        self.templateFidSelectorTB.noneEnabled = True
        self.templateFidSelectorTB.showHidden = False
        self.templateFidSelectorTB.showChildNodeTypes = False
        self.templateFidSelectorTB.setMRMLScene( slicer.mrmlScene )
        self.templateFidSelectorTB.setToolTip( "Pick template fiducials to register input volume fiducials to" )

        templateLayoutTB = qt.QHBoxLayout()
        templateLayoutTB.addWidget(self.templateAtlasSelectorTB)
        templateLayoutTB.addWidget(self.templateFidSelectorTB)
        parametersFormLayoutAlignTB.addRow("Atlas Template & Fiducials: ", templateLayoutTB)
        #
        # input volume selector
        #
        self.inputSelectorTB = slicer.qMRMLNodeComboBox()
        self.inputSelectorTB.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputSelectorTB.selectNodeUponCreation = True
        self.inputSelectorTB.addEnabled = False
        self.inputSelectorTB.removeEnabled = False
        self.inputSelectorTB.noneEnabled = True
        self.inputSelectorTB.showHidden = False
        self.inputSelectorTB.showChildNodeTypes = False
        self.inputSelectorTB.setMRMLScene( slicer.mrmlScene )
        self.inputSelectorTB.setToolTip( "Pick the volume to align " )
        parametersFormLayoutAlignTB.addRow("Align Input Volume: ", self.inputSelectorTB)

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
        parametersFormLayoutAlignTB.addRow("Fiduical Placement: ", fiduicalPlacement1)

        fiduicalPlacement2 = qt.QHBoxLayout()
        fiduicalPlacement2.addWidget(self.AEButton)
        fiduicalPlacement2.addWidget(self.PSCButton)
        parametersFormLayoutAlignTB.addRow("Fiduical Placement: ", fiduicalPlacement2)

        fiduicalPlacement3 = qt.QHBoxLayout()
        fiduicalPlacement3.addWidget(self.OWButton)
        fiduicalPlacement3.addWidget(self.RWButton)
        parametersFormLayoutAlignTB.addRow("Fiduical Placement: ", fiduicalPlacement3)


        #
        # Align Button
        #
        self.alignButtonTB = qt.QPushButton("Align")
        self.alignButtonTB.toolTip = "Align volume to clinical reference"
        self.alignButtonTB.enabled = False
        parametersFormLayoutAlignTB.addRow(self.alignButtonTB)


        #
        #Crop Volume AREA
        #
        parametersCollapsibleButtonCrop = ctk.ctkCollapsibleButton()
        parametersCollapsibleButtonCrop.text = "Crop Volume"
        self.layout.addWidget(parametersCollapsibleButtonCrop)

        # Layout within the Crop collapsible button
        parametersFormLayoutCrop = qt.QFormLayout(parametersCollapsibleButtonCrop)


        #
        # input template volume template selector
        #
        self.cropTemplateSelector = slicer.qMRMLNodeComboBox()
        self.cropTemplateSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.cropTemplateSelector.selectNodeUponCreation = True
        self.cropTemplateSelector.addEnabled = False
        self.cropTemplateSelector.removeEnabled = False
        self.cropTemplateSelector.noneEnabled = True
        self.cropTemplateSelector.showHidden = False
        self.cropTemplateSelector.showChildNodeTypes = False
        self.cropTemplateSelector.setMRMLScene( slicer.mrmlScene )
        self.cropTemplateSelector.setToolTip( "select crop template volume " )
        parametersFormLayoutCrop.addRow("Crop Template Volume: ", self.cropTemplateSelector)



        #
        # input crop volume template selector
        #
        self.cropInputSelector = slicer.qMRMLNodeComboBox()
        self.cropInputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.cropInputSelector.selectNodeUponCreation = True
        self.cropInputSelector.addEnabled = False
        self.cropInputSelector.removeEnabled = False
        self.cropInputSelector.noneEnabled = True
        self.cropInputSelector.showHidden = False
        self.cropInputSelector.showChildNodeTypes = False
        self.cropInputSelector.setMRMLScene( slicer.mrmlScene )
        self.cropInputSelector.setToolTip( "select input volume " )
        parametersFormLayoutCrop.addRow("Crop Input Volume: ", self.cropInputSelector)


        #
        #Define ROI & Crop buttons
        #
        self.defineCropButton		 	= qt.QPushButton('Define ROI')
        self.defineCropButton.toolTip 	= "Define region of interest for cropping"
        self.defineCropButton.enabled	= False

        self.cropButton		 	        = qt.QPushButton('Crop!')
        self.cropButton.toolTip 	    = "Crop input volume"
        self.cropButton.enabled	        = False

        imageCropping = qt.QHBoxLayout()
        imageCropping.addWidget(self.defineCropButton)
        imageCropping.addWidget(self.cropButton)
        parametersFormLayoutCrop.addRow("Select & Crop Region of Interest: ", imageCropping)

        #
        # Volume connections
        #

        # Cochlear Only
        self.templateAtlasSelectorCO.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlignCO)
        self.templateFidSelectorCO.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlignCO)
        self.inputSelectorCO.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlignCO)
        self.OWButtonCO.connect('clicked(bool)', self.onOWButtonCO)
        self.CNButton.connect('clicked(bool)', self.onCNButton)
        self.AButton.connect('clicked(bool)', self.onAButton)
        self.RWButtonCO.connect('clicked(bool)', self.onRWButtonCO)
        self.alignButtonCO.connect('clicked(bool)', self.onAlignButtonCO)

        # Temporal Bone
        self.templateAtlasSelectorTB.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlignTB)
        self.templateFidSelectorTB.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlignTB)
        self.inputSelectorTB.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectAlignTB)
        self.PAButton.connect('clicked(bool)', self.onPAButton)
        self.GGButton.connect('clicked(bool)', self.onGGButton)
        self.SFButton.connect('clicked(bool)', self.onSFButton)
        self.AEButton.connect('clicked(bool)', self.onAEButton)
        self.PSCButton.connect('clicked(bool)', self.onPSCButton)
        self.OWButton.connect('clicked(bool)', self.onOWButton)
        self.RWButton.connect('clicked(bool)', self.onRWButton)
        self.alignButtonTB.connect('clicked(bool)', self.onAlignButtonTB)

        #Crop Volumes
        self.cropTemplateSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectCrop)
        self.cropInputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectCrop)
        self.defineCropButton.connect('clicked(bool)', self.onDefineCropButton)
        self.cropButton.connect('clicked(bool)', self.onCropButton)

        # Add vertical spacer
        self.layout.addStretch(1)

        # Refresh select buttons' state
        self.onSelectAlignCO()
        self.onSelectAlignTB()
        self.onSelectCrop()

    #Align Cochlear Only Buttons
    def onOWButtonCO(self):

        #initialize placement checklist
        self.placementListCO = {'OW': True, 'CN': True, 'A': True,'RW': True} #Tracking skipped fiducial

        #Setup Fiduical placement
        self.movingFiducialNodeCO = slicer.vtkMRMLMarkupsFiducialNode()
        slicer.mrmlScene.AddNode(self.movingFiducialNodeCO)

        #Fiduical Placement Widget
        self.fiducialWidgetCO = slicer.qSlicerMarkupsPlaceWidget()
        self.fiducialWidgetCO.buttonsVisible = False
        self.fiducialWidgetCO.placeButton().show()
        self.fiducialWidgetCO.setMRMLScene(slicer.mrmlScene)
        self.fiducialWidgetCO.setCurrentNode(self.movingFiducialNodeCO)
        self.fiducialWidgetCO.placeMultipleMarkups = slicer.qSlicerMarkupsPlaceWidget.ForcePlaceSingleMarkup

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Oval Window:\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidgetCO.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.OWButtonCO.enabled = False
            self.CNButton.enabled = True
        else:
            self.placementListCO['OW'] = False
            #Enable/Disable Buttons
            self.OWButtonCO.enabled = False
            self.CNButton.enabled = True

    def onCNButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Cochlear Nerve:\n\n" +
                                            "YES - To place fiducial\n"
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidgetCO.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.CNButton.enabled = False
            self.AButton.enabled = True
        else:
            self.placementListCO['CN'] = False
            #Enable/Disable Buttons
            self.CNButton.enabled = False
            self.AButton.enabled = True


    def onAButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Apex:\n\n" +
                                            "YES - To place fiducial\n"
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidgetCO.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.AButton.enabled = False
            self.RWButtonCO.enabled = True
        else:
            self.placementListCO['A'] = False
            #Enable/Disable Buttons
            self.AButton.enabled = False
            self.RWButtonCO.enabled = True


    def onRWButtonCO(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Round Window:\n\n" +
                                            "YES - To place fiducial\n"
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidgetCO.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.RWButtonCO.enabled = False
            self.alignButtonCO.enabled = True
        else:
            self.placementListCO['RW'] = False
            #Enable/Disable Buttons
            self.RWButtonCO.enabled = False
            self.alignButtonCO.enabled = True


    def onAlignButtonCO(self):

        self.RWButtonCO.enabled = False
        self.alignButtonCO.enabled = False

        self.landmarkTransformCO = slicer.vtkMRMLTransformNode()
        slicer.mrmlScene.AddNode(self.landmarkTransformCO)

        logic = AlignCrop3DSlicerModuleLogic()
        if(self.movingFiducialNodeCO.GetNumberOfFiducials() > 2):
            logic.runAlignmentRegistration(self.landmarkTransformCO, self.templateFidCO, self.movingFiducialNodeCO, self.placementListCO)
        else:
            slicer.util.infoDisplay("At least 3 fiducials required for registration to proceed")

        #Apply Landmark transform on input Volume & Fiducials and Harden
        self.inputVolumeCO.SetAndObserveTransformNodeID(self.landmarkTransformCO.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.inputVolumeCO)
        self.movingFiducialNodeCO.SetAndObserveTransformNodeID(self.landmarkTransformCO.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.movingFiducialNodeCO)


        #Set template to foreground in Slice Views
        applicationLogic 	= slicer.app.applicationLogic()
        selectionNode 		= applicationLogic.GetSelectionNode()
        selectionNode.SetSecondaryVolumeID(self.templateVolumeCO.GetID())
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

        #centre slice viewer on image
        slicer.app.applicationLogic().FitSliceToAll()

    #Align Temporal Bone Buttons
    def onPAButton(self):

        #initialize placement checklist
        self.placementListTB = {'PA': True, 'GG': True, 'SF': True,'AE': True,'PSC': True,'OW': True,'RW': True} #Tracking skipped fiducial

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

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Porus Acousticus:\n\n" +
                                            "Place fiducial on the centre of the porus acousticus.\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.PAButton.enabled = False
            self.GGButton.enabled = True
        else:
            self.placementListTB['PA'] = False
            #Enable/Disable Buttons
            self.PAButton.enabled = False
            self.GGButton.enabled = True


    def onGGButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Geniculate Ganglion:\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.GGButton.enabled = False
            self.SFButton.enabled = True
        else:
            self.placementListTB['GG'] = False
            #Enable/Disable Buttons
            self.GGButton.enabled = False
            self.SFButton.enabled = True


    def onSFButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Stylomastoid Foramen:\n\n" +
                                            "place fiducial at the point it becomes the canal.\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.SFButton.enabled = False
            self.AEButton.enabled = True
        else:
            self.placementListTB['GG'] = False
            #Enable/Disable Buttons
            self.SFButton.enabled = False
            self.AEButton.enabled = True


    def onAEButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Arcuate Eminence:\n\n" +
                                            "Place fiducial on the centre of the top of the superior semicircular canal.\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.AEButton.enabled = False
            self.PSCButton.enabled = True
        else:
            self.placementListTB['AE'] = False
            #Enable/Disable Buttons
            self.AEButton.enabled = False
            self.PSCButton.enabled = True


    def onPSCButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Posterior Semicircular Canal:\n\n" +
                                            "Place fiduical on the mid point of the posterior semicircular canal.\n\n"
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.PSCButton.enabled = False
            self.OWButton.enabled = True
        else:
            self.placementListTB['PSC'] = False
            #Enable/Disable Buttons
            self.PSCButton.enabled = False
            self.OWButton.enabled = True


    def onOWButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Oval Window:\n\n" +
                                            "Place fiducial on the centre of the oval window.\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.OWButton.enabled = False
            self.RWButton.enabled = True
        else:
            self.placementListTB['OW'] = False
            #Enable/Disable Buttons
            self.OWButton.enabled = False
            self.RWButton.enabled = True


    def onRWButton(self):

        placeCurrentFid = slicer.util.confirmYesNoDisplay("Round Window:\n\n" +
                                            "Place fiduical on the centre of the round window.\n\n" +
                                            "YES - To place fiducial\n" +
                                            "NO - To skip current fiducial\n" )

        if placeCurrentFid == True:
            #Enable fiducial placement
            self.fiducialWidget.setPlaceModeEnabled(True)
            #Enable/Disable Buttons
            self.RWButton.enabled       = False
            self.alignButtonTB.enabled  = True
        else:
            self.placementListTB['RW'] = False
            #Enable/Disable Buttons
            self.RWButton.enabled       = False
            self.alignButtonTB.enabled  = True


    def onAlignButtonTB(self):

        self.RWButton.enabled = False
        self.alignButtonTB.enabled = False

        self.landmarkTransform = slicer.vtkMRMLTransformNode()
        slicer.mrmlScene.AddNode(self.landmarkTransform)

        logic = AlignCrop3DSlicerModuleLogic()
        if(self.movingFiducialNode.GetNumberOfFiducials() > 2):
            logic.runAlignmentRegistration(self.landmarkTransform, self.templateFidTB, self.movingFiducialNode, self.placementListTB)
        else:
            slicer.util.infoDisplay("At least 3 fiducials required for registration to proceed")

        #Apply Landmark transform on input Volume & Fiducials and Harden
        self.inputVolumeTB.SetAndObserveTransformNodeID(self.landmarkTransform.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.inputVolumeTB)
        self.movingFiducialNode.SetAndObserveTransformNodeID(self.landmarkTransform.GetID())
        slicer.vtkSlicerTransformLogic().hardenTransform(self.movingFiducialNode)


        #TODO - Align output is incorrect!! Investigate (Jan 17th - 2018)

        #Set template to foreground in Slice Views
        applicationLogic 	= slicer.app.applicationLogic()
        selectionNode 		= applicationLogic.GetSelectionNode()
        selectionNode.SetSecondaryVolumeID(self.templateVolumeTB.GetID())
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

        #centre slice viewer on image
        slicer.app.applicationLogic().FitSliceToAll()
        #Make Atlas Fidcials visible
        self.templateFidTB.SetDisplayVisibility(1)


    #Cropping Buttons
    def onDefineCropButton(self):

        #Define logic & retrieve atlas/template region of interest (ROI)
        logic = AlignCrop3DSlicerModuleLogic()
        self.templateROI = logic.runDefineCropROIVoxel(self.cropTemplateVolume)

        #Enable cropping button
        self.cropButton.enabled = True

    def onCropButton(self):

        #cropVolume
        logic = AlignCrop3DSlicerModuleLogic()
        logic.runCropVolume(    self.templateROI,
                                self.cropInputSelector.currentNode())


        #TODO - setup layout on slicer view after cropping.
        #centre slice viewer on image
        slicer.app.applicationLogic().FitSliceToAll()

        self.cropButton.enabled = False

    def cleanup(self):
        pass

    def onSelectAlignCO(self):
        self.OWButtonCO.enabled =  self.templateAtlasSelectorCO.currentNode() and self.templateFidSelectorCO.currentNode() and self.inputSelectorCO.currentNode()

        if(self.OWButtonCO.enabled):
            self.inputVolumeCO    = self.inputSelectorCO.currentNode()
            self.templateVolumeCO = self.templateAtlasSelectorCO.currentNode()
            self.templateFidCO    = self.templateFidSelectorCO.currentNode()
            #Make Atlas Fidcials not visible
            self.templateFidCO.SetDisplayVisibility(0)

    def onSelectAlignTB(self):
        self.PAButton.enabled =  self.templateAtlasSelectorTB.currentNode() and self.templateFidSelectorTB.currentNode() and self.inputSelectorTB.currentNode()

        if(self.PAButton.enabled):
            self.inputVolumeTB    = self.inputSelectorTB.currentNode()
            self.templateVolumeTB = self.templateAtlasSelectorTB.currentNode()
            self.templateFidTB    = self.templateFidSelectorTB.currentNode()
            #Make Atlas Fidcials not visible
            self.templateFidTB.SetDisplayVisibility(0)

    def onSelectCrop(self):
        self.defineCropButton.enabled = self.cropTemplateSelector.currentNode() and self.cropInputSelector.currentNode()

        if(self.defineCropButton.enabled):
            self.cropTemplateVolume = self.cropTemplateSelector.currentNode()
            self.cropInputVolume    = self.cropInputSelector.currentNode()


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

    def runAlignmentRegistration(self, transform, fixedFiducial, movingFiducial, placementChecklist):

        logging.info("Now running Alignment Registration")

        #deselected unused fiducials
        if len(placementChecklist) == 4:
            for key, value in placementChecklist.iteritems():
                if value != True:
                    if key == 'OW':
                        fixedFiducial.SetNthFiducialSelected(0, 0)
                    if key == 'CN':
                        fixedFiducial.SetNthFiducialSelected(1, 0)
                    if key == 'A':
                        fixedFiducial.SetNthFiducialSelected(2, 0)
                    if key == 'RW':
                        fixedFiducial.SetNthFiducialSelected(3, 0)
        else:
            for key, value in placementChecklist.iteritems():
                if value != True:
                    if key == 'PA':
                        fixedFiducial.SetNthFiducialSelected(0, 0)
                    if key == 'GG':
                        fixedFiducial.SetNthFiducialSelected(1, 0)
                    if key == 'SF':
                        fixedFiducial.SetNthFiducialSelected(2, 0)
                    if key == 'AE':
                        fixedFiducial.SetNthFiducialSelected(3, 0)
                    if key == 'PSC':
                        fixedFiducial.SetNthFiducialSelected(4, 0)
                    if key == 'OW':
                        fixedFiducial.SetNthFiducialSelected(5, 0)
                    if key == 'RW':
                        fixedFiducial.SetNthFiducialSelected(6, 0)

        #Setup and Run Landmark Registration
        cliParamsFidReg = {	'fixedLandmarks'	: fixedFiducial.GetID(),
		                    'movingLandmarks' 	: movingFiducial.GetID(),
		                    'TransformType' 	: 'Rigid',
		                    'saveTransform' 	: transform.GetID() }

        cliRigTrans = slicer.cli.run( slicer.modules.fiducialregistration, None,
		                              cliParamsFidReg, wait_for_completion=True )


    def runDefineCropROI(self, cropParam):
        """
        Function used if ROI is not to be voxel based -
        - Function is not used in this .py script
        - Function can be used for future development
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

    def runDefineCropROIVoxel(self, inputVol):

        #create crop volume parameter node
        cropParamNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropParamNode.SetScene(slicer.mrmlScene)
        cropParamNode.SetName('Template_ROI')
        cropParamNode.SetInputVolumeNodeID(inputVol.GetID())

        #create ROI
        template_roi = slicer.vtkMRMLAnnotationROINode()
        slicer.mrmlScene.AddNode(template_roi)
        cropParamNode.SetROINodeID(template_roi.GetID())

        #Fit roi to input image
        slicer.mrmlScene.AddNode(cropParamNode)
        slicer.modules.cropvolume.logic().SnapROIToVoxelGrid(cropParamNode)
        slicer.modules.cropvolume.logic().FitROIToInputVolume(cropParamNode)

        return template_roi

    def runCropVolume(self, roi, volume):

        logging.info('Cropping processing started')

        #Create Crop Volume Parameter node
        cropParamNode = slicer.vtkMRMLCropVolumeParametersNode()
        cropParamNode.SetScene(slicer.mrmlScene)
        cropParamNode.SetName('Crop_volume_Node1')
        cropParamNode.SetInputVolumeNodeID(volume.GetID())
        cropParamNode.SetROINodeID(roi.GetID())
        slicer.mrmlScene.AddNode(cropParamNode)

        #Apply Cropping
        slicer.modules.cropvolume.logic().Apply(cropParamNode)

        logging.info('Cropping processing completed')



class AlignCrop3DSlicerModuleTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  #TODO Need to implement appropiate test cases - Class left untouched

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
