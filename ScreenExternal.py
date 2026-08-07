from CvPythonExtensions import *


import json_parser
import time

def logToFile(message, filename="mylog.txt"):
	f = open(filename, "a")  # append mode
	f.write("%s at [%s]\n" % (message, time.ctime()))
	f.close()
	
class ScreenExternal:
	def __init__(self, civilopedia_data=None, techchooser_data=None, build_page_link=None):
		self.CivilopediaData = civilopedia_data or {
			"title": "Civilopedia",
			"Categories": []
		}
		self.TechChooserData = techchooser_data or {
			"title": "TechChooser",
			"Techs": [],
			"Arrows": [],
			"TechNames": []
		}
		self.buildPageLink = build_page_link
		self.name = "i am an external Screen"
		logToFile("%s instance created" % self.name)
  
	def saveCivilopediaDataToFile(self, filename):
		json_parser.write_json(self.CivilopediaData, filename)
	def saveTechChooserDataToFile(self, filename):
		json_parser.write_json(self.TechChooserData, filename)
	
	def addToLastPediaPanelEntry(self, data):
		if self.CivilopediaData["Categories"] != []:
			self.CivilopediaData["Categories"][-1]["Entries"][-1]["PageContent"][-1]["content"].append(data)
	
	def addToUpgradeGraph(self, data):
		# since the update graph is simply supposed to be a Page with only one Panel, 
		# we can handle it the same way as any other Page.
		self.addToLastPediaPanelEntry(data)
   
	def addToLastTechChooserPanelEntry(self, data):
		if self.TechChooserData["Techs"] != []:
			self.TechChooserData["Techs"][-1]["content"].append(data)
   
	def addArrowToTechChooser(self, data):
		self.TechChooserData["Arrows"].append(data)
	
	

	## ----------------------- Overrides of CyGInterfaceScreen methods -----------------------
	def addPanel(self, *args, **kwargs):
		logToFile('addPanel was called')
		logToFile('with args: %s' % str(args))
		panelData = {
			"title": args[1],
			"content": [],
			"type": "panel"
		}
		# calls to addPanel() from the TechChooser will be ignored.
		if self.CivilopediaData["Categories"] != []:
			self.CivilopediaData["Categories"][-1]["Entries"][-1]["PageContent"].append(panelData)
		
	def addListBoxGFC(self, *args, **kwargs):
		# listboxes will be interpretes as panels
		logToFile('addListBoxGFC was called')
		logToFile('with args: %s' % str(args))
		panelData = {
					"title": args[1],
					"content": [],
					"type": "listbox"
				}
		if self.CivilopediaData["Categories"] != []:
			self.CivilopediaData["Categories"][-1]["Entries"][-1]["PageContent"].append(panelData)

	def addMultilineText(self, *args, **kwargs):
		logToFile('addMultilineText was called')
		logToFile('with args: %s' % str(args))
		self.addToLastPediaPanelEntry({"type": "text", "text": args[1]})
		pass
	
	def attachLabel(self, *args, **kwargs):
		logToFile('attachLabel was called')
		self.addToLastPediaPanelEntry({"type": "text", "text": args[2]})
		pass
		
	def attachImageButton(self, *args, **kwargs):
		logToFile('attachImageButton was called')
		logToFile('with args: %s' % str(args))
  
		link = self.buildPageLink(str(args[4]), args[5])
		buttonData = {	
					"type": "buttonlink",
					"source": args[2],
					
				}
		if link != "":
			buttonData["link"] = link
			buttonData["linkCategory"] = str(args[4])
			buttonData["linkEntry"] = args[5]
		self.addToLastPediaPanelEntry(buttonData)
		

	def addDDSGFC(self, *args, **kwargs):
		logToFile('addDDSGFC was called')
		logToFile('with args: %s' % str(args))
		self.addToLastPediaPanelEntry({"type": "button", "source": args[1]})
		pass

	def appendListBoxString(self, *args, **kwargs):
		logToFile('appendListBoxString was called')
		logToFile('with args: %s' % str(args))
		self.addToLastPediaPanelEntry({"type": "listboxstring", "text": args[1]})
		pass

	def setTableText(self, *args, **kwargs):
		logToFile('setTableText was called')
		logToFile('with args: %s' % str(args))
		# no table will be created. the table text will be interpreted as a simple button.
		if "WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT" == str(args[5]):
			self.addToLastPediaPanelEntry({"type": "button", "source": args[4]})
		pass

#### Used for arrows in unit and promotion upgrade trees and the techchooser. #####
	def addDDSGFCAt(self, *args, **kwargs):
		logToFile('addDDSGFCAt was called')
		logToFile('with args: %s' % str(args))
		# basically buttons. exept arrows.
		link = self.buildPageLink(str(args[7]), args[8])
  
		buttonData = {
						"type": "buttonlinkAt",
						"source": args[2],
						"x": args[3], 
						"y": args[4], 
						"width": args[5], 
						"height": args[6]
						}
		if link != "":
			# if link is empty, the button will not be added to the page.
			buttonData["link"] = link
			buttonData["linkCategory"] = str(args[7])
			buttonData["linkEntry"] = args[8]
		if args[1] == "TechList":
			# Techchooser arrows
			self.addArrowToTechChooser(buttonData)
		elif args[1].startswith("TechBox"):
			# addition to a TechChooser panel/ a Techbox
			self.addToLastTechChooserPanelEntry(buttonData)
		else:
			# Unit/Promotions Upgrade Graph lines
			self.addToUpgradeGraph(buttonData)
		
## used to place the unit and promotion buttons in the unit and promotion upgrade trees. ##
	def setImageButtonAt(self, *args, **kwargs):
		logToFile('setImageButtonAt was called')
		logToFile('with args: %s' % str(args))
		link = self.buildPageLink(str(args[7]), args[8])
		buttonData = {
						"type": "buttonlinkAt",
						"source": args[2],
						"x": args[3], 
						"y": args[4], 
						"width": args[5], 
						"height": args[6]
						}
		if link != "":
			# if link is empty, the button will not be added to the page.
			buttonData["link"] = link
			buttonData["linkCategory"] = str(args[7])
			buttonData["linkEntry"] = args[8]
		self.addToUpgradeGraph(buttonData)
		
#####################################################
#### Used in the Techchooser. #####
	def attachPanelAt(self, *args, **kwargs):
		logToFile('attachPanelAt was called')

		# add TechChooser panel to TechChooserData
		panelData = {
			"title": args[1],
			"id": args[1].replace("TechBox", "TechID"),
			"content": [],
			"type": "TechChooserPanel",
			"x": args[7], # x, y, width, height
			"y": args[8],
			"width": args[9],
			"height": args[10]
		}
		self.TechChooserData["Techs"].append(panelData)
  
	# for setting the name of a tech
	# save the szTechID (args[0]) here and for the Tech in attachPanelAt(), so one can later assign them properly
	def setTextAt(self, *args, **kwargs):
		logToFile('setTextAt was called')
		LabelData = {
			"type": "TechBoxLabel",
			"id": args[0],
			"text": args[2],
			"x": args[4],
			"y": args[5],
		}
		# find the corresponding TechChooser panel and assign the label to it

		TechBox = None
		for tech in self.TechChooserData["Techs"]:
			if tech.get("id") == args[0]:
				TechBox = tech
				break
		if TechBox:
			TechBox["content"].append(LabelData)
  

#####################################################
	def getXResolution(self, *args, **kwargs):
		logToFile('getXResolution was called')
		return 0
	
	def getYResolution(self, *args, **kwargs):
		logToFile('getYResolution was called')
		return 0

	def addBonusGraphicGFC(self, *args, **kwargs):
		logToFile('addBonusGraphicGFC was called')
		pass

	def addBuildingGraphicGFC(self, *args, **kwargs):
		logToFile('addBuildingGraphicGFC was called')
		pass

	def addCheckBoxGFC(self, *args, **kwargs):
		logToFile('addCheckBoxGFC was called')
		pass

	def addCheckBoxGFCAt(self, *args, **kwargs):
		logToFile('addCheckBoxGFCAt was called')
		pass

	def addDrawControl(self, *args, **kwargs):
		logToFile('addDrawControl was called')
		pass

	def addDropDownBoxGFC(self, *args, **kwargs):
		logToFile('addDropDownBoxGFC was called')
		pass

	def addFlagWidgetGFC(self, *args, **kwargs):
		logToFile('addFlagWidgetGFC was called')
		pass

	def addGraphData(self, *args, **kwargs):
		logToFile('addGraphData was called')
		pass

	def addGraphLayer(self, *args, **kwargs):
		logToFile('addGraphLayer was called')
		pass

	def addGraphWidget(self, *args, **kwargs):
		logToFile('addGraphWidget was called')
		pass

	def addImprovementGraphicGFC(self, *args, **kwargs):
		logToFile('addImprovementGraphicGFC was called')
		pass

	def addLeaderheadGFC(self, *args, **kwargs):
		logToFile('addLeaderheadGFC was called')
		pass

	def addLineGFC(self, *args, **kwargs):
		logToFile('addLineGFC was called')
		pass

	def addModelGraphicGFC(self, *args, **kwargs):
		logToFile('addModelGraphicGFC was called')
		pass

	def addMultiListControlGFC(self, *args, **kwargs):
		logToFile('addMultiListControlGFC was called')
		pass

	def addPlotGraphicGFC(self, *args, **kwargs):
		logToFile('addPlotGraphicGFC was called')
		pass

	def addPullDownString(self, *args, **kwargs):
		logToFile('addPullDownString was called')
		pass

	def addScrollPanel(self, *args, **kwargs):
		logToFile('addScrollPanel was called')
		pass

	def addSlider(self, *args, **kwargs):
		logToFile('addSlider was called')
		pass

	def addSpaceShipWidgetGFC(self, *args, **kwargs):
		logToFile('addSpaceShipWidgetGFC was called')
		pass

	def addSpecificUnitGraphicGFC(self, *args, **kwargs):
		logToFile('addSpecificUnitGraphicGFC was called')
		pass

	def addStackedBarGFC(self, *args, **kwargs):
		logToFile('addStackedBarGFC was called')
		pass

	def addStackedBarGFCAt(self, *args, **kwargs):
		logToFile('addStackedBarGFCAt was called')
		pass

	def addTab(self, *args, **kwargs):
		logToFile('addTab was called')
		pass

	def addTableControlGFC(self, *args, **kwargs):
		logToFile('addTableControlGFC was called')
		pass

	def addToModelGraphicGFC(self, *args, **kwargs):
		logToFile('addToModelGraphicGFC was called')
		pass

	def addUnitGraphicGFC(self, *args, **kwargs):
		logToFile('addUnitGraphicGFC was called')
		pass

	def appendListBoxStringNoUpdate(self, *args, **kwargs):
		logToFile('appendListBoxStringNoUpdate was called')
		pass

	def appendMultiListButton(self, *args, **kwargs):
		logToFile('appendMultiListButton was called')
		pass

	def appendTableRow(self, *args, **kwargs):
		logToFile('appendTableRow was called')
		pass

	def attachButton(self, *args, **kwargs):
		logToFile('attachButton was called')
		pass

	def attachCheckBox(self, *args, **kwargs):
		logToFile('attachCheckBox was called')
		pass

	def attachControlToTableCell(self, *args, **kwargs):
		logToFile('attachControlToTableCell was called')
		pass

	def attachDropDown(self, *args, **kwargs):
		logToFile('attachDropDown was called')
		pass

	def attachEdit(self, *args, **kwargs):
		logToFile('attachEdit was called')
		pass

	def attachHBox(self, *args, **kwargs):
		logToFile('attachHBox was called')
		pass

	def attachHSeparator(self, *args, **kwargs):
		logToFile('attachHSeparator was called')
		pass

	def attachHSlider(self, *args, **kwargs):
		logToFile('attachHSlider was called')
		pass

	def attachListBoxGFC(self, *args, **kwargs):
		logToFile('attachListBoxGFC was called')
		pass

	def attachMultiListControlGFC(self, *args, **kwargs):
		logToFile('attachMultiListControlGFC was called')
		pass

	def attachMultilineText(self, *args, **kwargs):
		logToFile('attachMultilineText was called')
		pass

	def attachPanel(self, *args, **kwargs):
		logToFile('attachPanel was called')
		pass

	def attachScrollPanel(self, *args, **kwargs):
		logToFile('attachScrollPanel was called')
		pass

	def attachSpacer(self, *args, **kwargs):
		logToFile('attachSpacer was called')
		pass

	def attachTabItem(self, *args, **kwargs):
		logToFile('attachTabItem was called')
		pass

	def attachTextGFC(self, *args, **kwargs):
		logToFile('attachTextGFC was called')
		pass

	def attachVBox(self, *args, **kwargs):
		logToFile('attachVBox was called')
		pass

	def attachVSeparator(self, *args, **kwargs):
		logToFile('attachVSeparator was called')
		pass

	def attachVSlider(self, *args, **kwargs):
		logToFile('attachVSlider was called')
		pass

	def back(self, *args, **kwargs):
		logToFile('back was called')
		pass

	def bringMinimapToFront(self, *args, **kwargs):
		logToFile('bringMinimapToFront was called')
		pass
	
	def centerY(self, *args, **kwargs):
		logToFile('centerY was called')
		pass

	def centerX(self, *args, **kwargs):
		logToFile('centerX was called')
		pass

	def changeDDSGFC(self, *args, **kwargs):
		logToFile('changeDDSGFC was called')
		pass

	def changeImageButton(self, *args, **kwargs):
		logToFile('changeImageButton was called')
		pass

	def clearGraphData(self, *args, **kwargs):
		logToFile('clearGraphData was called')
		pass

	def clearListBoxGFC(self, *args, **kwargs):
		logToFile('clearListBoxGFC was called')
		pass

	def clearMultiList(self, *args, **kwargs):
		logToFile('clearMultiList was called')
		pass

	def deleteWidget(self, *args, **kwargs):
		logToFile('deleteWidget was called')
		pass

	def disableMultiListButton(self, *args, **kwargs):
		logToFile('disableMultiListButton was called')
		pass

	def enable(self, *args, **kwargs):
		logToFile('enable was called')
		pass

	def enableMultiListPulse(self, *args, **kwargs):
		logToFile('enableMultiListPulse was called')
		pass

	def enableSelect(self, *args, **kwargs):
		logToFile('enableSelect was called')
		pass

	def enableSort(self, *args, **kwargs):
		logToFile('enableSort was called')
		pass

	def enableWorldSounds(self, *args, **kwargs):
		logToFile('enableWorldSounds was called')
		pass

	def foo(self, *args, **kwargs):
		logToFile('foo was called')
		pass

	def forward(self, *args, **kwargs):
		logToFile('forward was called')
		pass

	def getPullDownData(self, *args, **kwargs):
		logToFile('getPullDownData was called')
		pass

	def getSelectedPullDownID(self, *args, **kwargs):
		logToFile('getSelectedPullDownID was called')
		pass

	def getTableNumRows(self, *args, **kwargs):
		logToFile('getTableNumRows was called')
		pass

	def getTableText(self, *args, **kwargs):
		logToFile('getTableText was called')
		pass

	def handleInput(self, *args, **kwargs):
		logToFile('handleInput was called')
		pass

	def hide(self, *args, **kwargs):
		logToFile('hide was called')
		pass

	def hideEndTurn(self, *args, **kwargs):
		logToFile('hideEndTurn was called')
		pass

	def hideList(self, *args, **kwargs):
		logToFile('hideList was called')
		pass

	def hideScreen(self, *args, **kwargs):
		logToFile('hideScreen was called')
		pass

	def initMinimap(self, *args, **kwargs):
		logToFile('initMinimap was called')
		pass

	def interfaceScreen(self, *args, **kwargs):
		logToFile('interfaceScreen was called')
		pass

	def isActive(self, *args, **kwargs):
		logToFile('isActive was called')
		pass

	def isPersistent(self, *args, **kwargs):
		logToFile('isPersistent was called')
		pass

	def isRowSelected(self, *args, **kwargs):
		logToFile('isRowSelected was called')
		pass

	def methodName(self, *args, **kwargs):
		logToFile('methodName was called')
		pass

	def minimapClearAllFlashingTiles(self, *args, **kwargs):
		logToFile('minimapClearAllFlashingTiles was called')
		pass

	def minimapFlashPlot(self, *args, **kwargs):
		logToFile('minimapFlashPlot was called')
		pass

	def modifyLabel(self, *args, **kwargs):
		logToFile('modifyLabel was called')
		pass

	def modifyString(self, *args, **kwargs):
		logToFile('modifyString was called')
		pass

	def moveItem(self, *args, **kwargs):
		logToFile('moveItem was called')
		pass

	def moveToBack(self, *args, **kwargs):
		logToFile('moveToBack was called')
		pass

	def moveToFront(self, *args, **kwargs):
		logToFile('moveToFront was called')
		pass

	def onClose(self, *args, **kwargs):
		logToFile('onClose was called')
		pass

	def prependListBoxString(self, *args, **kwargs):
		logToFile('prependListBoxString was called')
		pass

	def registerHideList(self, *args, **kwargs):
		logToFile('registerHideList was called')
		pass

	def removeLineGFC(self, *args, **kwargs):
		logToFile('removeLineGFC was called')
		pass

	def resetStatus(self, *args, **kwargs):
		logToFile('resetStatus was called')
		pass

	def saveDataToFile(self, *args, **kwargs):
		logToFile('saveDataToFile was called')
		pass

	def scrollableAreaScrollToBottom(self, *args, **kwargs):
		logToFile('scrollableAreaScrollToBottom was called')
		pass

	def selectMultiList(self, *args, **kwargs):
		logToFile('selectMultiList was called')
		pass

	def selectRow(self, *args, **kwargs):
		logToFile('selectRow was called')
		pass

	def setActivation(self, *args, **kwargs):
		logToFile('setActivation was called')
		pass

	def setAlwaysShown(self, *args, **kwargs):
		logToFile('setAlwaysShown was called')
		pass

	def setBarPercentage(self, *args, **kwargs):
		logToFile('setBarPercentage was called')
		pass

	def setButtonGFC(self, *args, **kwargs):
		logToFile('setButtonGFC was called')
		pass

	def setCloseOnEscape(self, *args, **kwargs):
		logToFile('setCloseOnEscape was called')
		pass

	def setControlFlag(self, *args, **kwargs):
		logToFile('setControlFlag was called')
		pass

	def setDimensions(self, *args, **kwargs):
		logToFile('setDimensions was called')
		pass

	def setDying(self, *args, **kwargs):
		logToFile('setDying was called')
		pass

	def setEnabled(self, *args, **kwargs):
		logToFile('setEnabled was called')
		pass

	def setEndTurnState(self, *args, **kwargs):
		logToFile('setEndTurnState was called')
		pass

	def setFocus(self, *args, **kwargs):
		logToFile('setFocus was called')
		pass

	def setForcedRedraw(self, *args, **kwargs):
		logToFile('setForcedRedraw was called')
		pass

	def setGraphLabelX(self, *args, **kwargs):
		logToFile('setGraphLabelX was called')
		pass

	def setGraphLabelY(self, *args, **kwargs):
		logToFile('setGraphLabelY was called')
		pass

	def setGraphYDataRange(self, *args, **kwargs):
		logToFile('setGraphYDataRange was called')
		pass

	def setHelpTextArea(self, *args, **kwargs):
		logToFile('setHelpTextArea was called')
		pass

	def setHelpTextString(self, *args, **kwargs):
		logToFile('setHelpTextString was called')
		pass

	def setHitTest(self, *args, **kwargs):
		logToFile('setHitTest was called')
		pass

	def setImageButton(self, *args, **kwargs):
		logToFile('setImageButton was called')
		pass

	def setLabel(self, *args, **kwargs):
		logToFile('setLabel was called')
		pass

	def setLabelAt(self, *args, **kwargs):
		logToFile('setLabelAt was called')
		pass

	def setLayoutFlag(self, *args, **kwargs):
		logToFile('setLayoutFlag was called')
		pass

	def setListBoxStringGFC(self, *args, **kwargs):
		logToFile('setListBoxStringGFC was called')
		pass

	def setMainInterface(self, *args, **kwargs):
		logToFile('setMainInterface was called')
		pass

	def setMinimapColor(self, *args, **kwargs):
		logToFile('setMinimapColor was called')
		pass

	def setMinimapMap(self, *args, **kwargs):
		logToFile('setMinimapMap was called')
		pass

	def setMinimapMode(self, *args, **kwargs):
		logToFile('setMinimapMode was called')
		pass

	def setPanelColor(self, *args, **kwargs):
		logToFile('setPanelColor was called')
		pass

	def setPanelSize(self, *args, **kwargs):
		logToFile('setPanelSize was called')
		pass

	def setPersistent(self, *args, **kwargs):
		logToFile('setPersistent was called')
		pass

	def setRenderInterfaceOnly(self, *args, **kwargs):
		logToFile('setRenderInterfaceOnly was called')
		pass

	def setScreenGroup(self, *args, **kwargs):
		logToFile('setScreenGroup was called')
		pass

	def setSelectedListBoxStringGFC(self, *args, **kwargs):
		logToFile('setSelectedListBoxStringGFC was called')
		pass

	def setSound(self, *args, **kwargs):
		logToFile('setSound was called')
		pass

	def setSoundId(self, *args, **kwargs):
		logToFile('setSoundId was called')
		pass

	def setStackedBarColors(self, *args, **kwargs):
		logToFile('setStackedBarColors was called')
		pass

	def setStackedBarColorsAlpha(self, *args, **kwargs):
		logToFile('setStackedBarColorsAlpha was called')
		pass

	def setStackedBarColorsRGB(self, *args, **kwargs):
		logToFile('setStackedBarColorsRGB was called')
		pass

	def setState(self, *args, **kwargs):
		logToFile('setState was called')
		pass

	def setStatus(self, *args, **kwargs):
		logToFile('setStatus was called')
		pass

	def setStyle(self, *args, **kwargs):
		logToFile('setStyle was called')
		pass

	def setTableColumnHeader(self, *args, **kwargs):
		logToFile('setTableColumnHeader was called')
		pass

	def setTableColumnRightJustify(self, *args, **kwargs):
		logToFile('setTableColumnRightJustify was called')
		pass

	def setTableDate(self, *args, **kwargs):
		logToFile('setTableDate was called')
		pass

	def setTableInt(self, *args, **kwargs):
		logToFile('setTableInt was called')
		pass

	def setText(self, *args, **kwargs):
		logToFile('setText was called')
		pass

	def setToolTip(self, *args, **kwargs):
		logToFile('setToolTip was called')
		pass

	def show(self, *args, **kwargs):
		logToFile('show was called')
		pass

	def showEndTurn(self, *args, **kwargs):
		logToFile('showEndTurn was called')
		pass

	def showScreen(self, *args, **kwargs):
		logToFile('showScreen was called')
		pass

	def showWindowBackground(self, *args, **kwargs):
		logToFile('showWindowBackground was called')
		pass

	def update(self, *args, **kwargs):
		logToFile('update was called')
		pass

	def updateAppropriateCitySelection(self, *args, **kwargs):
		logToFile('updateAppropriateCitySelection was called')
		pass

	def updateListBox(self, *args, **kwargs):
		logToFile('updateListBox was called')
		pass

	def updateMinimap(self, *args, **kwargs):
		logToFile('updateMinimap was called')
		pass

	def updateMinimapColorFromMap(self, *args, **kwargs):
		logToFile('updateMinimapColorFromMap was called')
		pass

	def updateMinimapSection(self, *args, **kwargs):
		logToFile('updateMinimapSection was called')
		pass

	def updateMinimapVisibility(self, *args, **kwargs):
		logToFile('updateMinimapVisibility was called')
		pass

