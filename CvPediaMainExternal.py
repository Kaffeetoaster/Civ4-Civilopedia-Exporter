import CvPediaMain
import CvTechChooser
import ScreenExternal
from CvScreenEnums import *

from CvPythonExtensions import *
from Consts import *
from RFCUtils import *

gc = CyGlobalContext()

import time

def logToFile(message, filename="myLogs/mylog.txt"):
	f = open(filename, "a")  # append mode
	f.write("%s at [%s]\n" % (message, time.ctime()))
	f.close()

def getUnitCategory(iUnit):
		'0 = Unit'
		'1 = Military Unit'
		'2 = Unique Unit'

		UnitInfo = gc.getUnitInfo(iUnit)
		UnitClassInfo = gc.getUnitClassInfo(UnitInfo.getUnitClassType())
		iDefaultUnit = UnitClassInfo.getDefaultUnitIndex()

		if UnitInfo.isGraphicalOnly() and not base_unit(iUnit) in [iWarrior, iAxeman, iSlave]:
			return -1
		elif iDefaultUnit > -1 and iDefaultUnit != iUnit and not iUnit == iAztecSlave:
			return 2
		elif UnitInfo.getCombat() > 0 or UnitInfo.getAirCombat() != 0 or UnitInfo.isSuicide():
			if not UnitInfo.isAnimal() and not UnitInfo.isFound():
				return 1

		return 0




class CvPediaMainExternal(CvPediaMain.CvPediaMain):
    
    def __init__(self):
        CvPediaMain.CvPediaMain.__init__(self)
        self.civilopedia_data = {
            "title": "Civilopedia",
            "Categories": []
        }
        
    def getScreen(self):
        return ScreenExternal.ScreenExternal(civilopedia_data=self.civilopedia_data, techchooser_data=None, build_page_link=buildPageLink)
        # is ScreenExternal() not enough?

    def CreateCivilopedia(self):
        """
        Creates the Civilopedia data structure by iterating through all categories and entries.
        For all categories exepect the upgrade trees this works by first collecting all data for a category 
        in self.list using the placeEntriesFunction. In a second step the data is displayed/added to the CivilopediaData structure 
        by calling the interfaceScreen function for each entry in self.list.
        For the upgrade trees the data is collected and displayed in one step, since this there is basically only one entry.
        """
        self.screen = self.getScreen()
        self.createScreen(self.screen)
        
        for i, (iCategory, placeEntriesFunction) in enumerate(self.mapListGenerators.items()):
            if iCategory in [PEDIA_UNIT_CATEGORIES, PEDIA_HINTS]:
                continue # There is something wrong with hints so we will leave it for now.
            if iCategory in [PEDIA_UNIT_UPGRADES, PEDIA_PROMOTION_TREE]:
                sCategory = self.categoryList[i][1]
                self.screen.CivilopediaData["Categories"].append({"Category": sCategory,
                                                                  "CategoryType": "UpgradeTree",
                                                                  "Entries": [{
                                                                        "title": sCategory,
                                                                        "PageContent": [{
                                                                                    "title": sCategory,
                                                                                    "content": [],
                                                                                    "type": "panel"
                                                                                }]
                                                                  }]})
                placeEntriesFunction()
                continue
                
            placeEntriesFunction() # for example placeCivs()
            
            # start new Category in ScreenExternal.CivilopediaData
            sCategory = self.categoryList[i][1]
            self.screen.CivilopediaData["Categories"].append({"Category": sCategory, "Entries": []})
            
            ## some logging
            logToFile("CvPediaMainExternal: %s list length: %d" % (sCategory, len(self.list)), filename="myLogs/print.txt")
            listasString = ",".join([str(i) for i in self.list])
            logToFile("CvPediaMainExternal: %s list as string: %s" % (sCategory, listasString), filename="myLogs/print.txt")
            ## end logging
            self.iCategory = iCategory
            func = self.mapScreenFunctions.get(iCategory)
            for i, iItem in enumerate(self.list):
                if iItem[1] != -1: # subcategories like "Ancient Era"  in the Techs have -1 as iItem
                    # start new entry for Category in ScreenExternal.CivilopediaData
                    self.screen.CivilopediaData["Categories"][-1]["Entries"].append({"title": iItem[0], "PageContent": []})
                    
                    func.interfaceScreen(iItem[1])
                # elif iItem[0] != "":
                #     self.screen.CivilopediaData["Categories"][-1]["Entries"].append({"title": "%s %s" % ("Subcategory:",iItem[0]), "PageContent": [{"title":iItem[0], "content": [], "type": "panel"}]})
                    
            self.screen.saveCivilopediaDataToFile("Export/CivilopediaData_raw.json")
            
class CvTechChooserExternal(CvTechChooser.CvTechChooser):
    def __init__(self):
        CvTechChooser.CvTechChooser.__init__(self)
        self.techchooser_data = {
            "title": "TechChooser",
            "Techs": [],
            "Arrows": []
        }
    # begin overrides of CvTechChooser methods
    def getScreen(self):
        return ScreenExternal.ScreenExternal(civilopedia_data=None, techchooser_data=self.techchooser_data, build_page_link=buildPageLink)
    
    def placeGreatPeople(self):
        pass
    # end overrides of CvTechChooser methods
    
    def CreateTechChooser(self):
        # init techchooser data structure.
        self.screen = self.getScreen()
        self.interfaceScreen() 
        self.screen.saveTechChooserDataToFile("Export/TechChooserData_raw.json")
        
        
        
        
# other effects, like map center, trading on ocean, obsolete bonus, reveal bonus
def buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId):
    #logToFile("buildPageLink: widgetName=%s, entryId=%s, HelpEntryId=%s => text=%s, function: %s " % (widgetName, entryId, HelpEntryId, TXT_KEY_HELP, funcHelp), filename="helptext_log.txt")
    
    
    if funcHelp is None or HelpEntryId == -1:
        description = ""
    else:
        try:
            description = funcHelp(HelpEntryId).getDescription()
        except Exception, e:
            logToFile("Error in buildHelpPreview: widgetName=%s, entryId=%s, HelpEntryId=%s => text=%s, function: %s, error: %s" % (widgetName, entryId, HelpEntryId, TXT_KEY_HELP, funcHelp, str(e)), filename="myLogs/helptext_log.txt")
            description = ""
    try:
        if TXT_KEY_HELP.startswith("TXT_KEY"):
            return "%s %s" % (CyTranslator().getText(TXT_KEY_HELP, ()), description)
        return "%s %s" % (TXT_KEY_HELP, description)
    except Exception, e:
        logToFile("Error in buildPageLink: widgetName=%s, entryId=%s, HelpEntryId=%s => text=%s, function: %s, error: %s" % (widgetName, entryId, HelpEntryId, TXT_KEY_HELP, funcHelp, str(e)), filename="myLogs/helptext_log.txt")
        return ""


def buildLink(infoGetter, txtKeyCategory, entryId):
    entryName = infoGetter(entryId).getDescription()
    categoryName = CyTranslator().getText(txtKeyCategory, ())
    return buildActualLink(categoryName, entryName)

def buildActualLink(CategoryName, entryName):
    return "%s#%s" % (CategoryName.replace(" ", "-"), entryName.replace(" ", "-"))


def buildPageLink(args):    
    # returns simply something like "Civ#Egypt" or "Tech#Pottery" for the given widgetName and entryId
    # also returns the help/preview text for the entry if available, otherwise None
    
    # probably some refactoring would make sense here, i guess
    
    widgetName, entryId, HelpEntryId = args
    previewText = ""

    # unit categories
    if widgetName == "WIDGET_PEDIA_JUMP_TO_UNIT":
        entryName = gc.getUnitInfo(entryId).getDescription()
        UnitCategory = getUnitCategory(entryId)
        if UnitCategory == 0:
            categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
        elif UnitCategory == 1:
            categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_MILITARY_UNITS", ())
        elif UnitCategory == 2:
            categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_UNITS", ())
        previewText = CyGameTextMgr().getUnitHelp(entryId, False, False, False, None)
        return buildActualLink(categoryName, entryName), previewText

    # building categories
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_BUILDING":
        entryName = gc.getBuildingInfo(entryId).getDescription()
        if entryName.startswith("The "): 
            entryName = entryName[4:] # remove "The " from the entry name. For wonders, kinda RFC DOC specific.
        
        buildingCategories = {
            0: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()),
            1: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGIOUS_BUILDINGS", ()),
            2: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_BUILDINGS", ()),
            3: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_GREAT_PEOPLE_BUILDINGS", ()),
            4: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_NATIONAL_WONDERS", ()),
            5: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_WORLD_WONDERS", ()),
        }
        categoryName = buildingCategories.get(getBuildingCategory(entryId))
        previewText = CyGameTextMgr().getBuildingHelp(entryId, False, False, False, None)
        return buildActualLink(categoryName, entryName), previewText

    
    
    # mod independent categories
    
    if widgetName == "WIDGET_PEDIA_JUMP_TO_CIV":
        previewText = CyGameTextMgr().parseCivInfos(entryId, False)
        return buildLink(gc.getCivilizationInfo, "TXT_KEY_PEDIA_CATEGORY_CIV",entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_LEADER":
        previewText = ""
        return buildLink(gc.getLeaderHeadInfo, "TXT_KEY_PEDIA_CATEGORY_LEADER", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_CIVIC":
        previewText = CyGameTextMgr().parseCivicInfo(entryId, False, False, False)
        return buildLink(gc.getCivicInfo, "TXT_KEY_PEDIA_CATEGORY_CIVIC", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_RELIGION":
        previewText = CyGameTextMgr().parseReligionInfo(entryId, False)
        return buildLink(gc.getReligionInfo, "TXT_KEY_PEDIA_CATEGORY_RELIGION", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_CORPORATIONS":
        previewText = CyGameTextMgr().parseCorporationInfo(entryId, False)
        return buildLink(gc.getCorporationInfo, "TXT_KEY_PEDIA_CATEGORY_CORPORATION", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_TECH":
        previewText = CyGameTextMgr().getTechHelp(entryId, False, False, False, False, -1)
        return buildLink(gc.getTechInfo, "TXT_KEY_PEDIA_CATEGORY_TECH", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH":
        previewText = CyGameTextMgr().getTechHelp(entryId, False, False, False, False, -1)
        return buildLink(gc.getTechInfo, "TXT_KEY_PEDIA_CATEGORY_TECH", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_DERIVED_TECH":
        previewText = CyGameTextMgr().getTechHelp(entryId, False, False, False, False, -1)
        return buildLink(gc.getTechInfo, "TXT_KEY_PEDIA_CATEGORY_TECH", entryId), previewText

    elif widgetName == "WIDGET_TECH_TREE":
        previewText = CyGameTextMgr().getTechHelp(entryId, False, False, False, False, -1)
        return buildLink(gc.getTechInfo, "TXT_KEY_PEDIA_CATEGORY_TECH", entryId), previewText

    elif widgetName == "WIDGET_HELP_TECH_PREPREQ":
        previewText = CyGameTextMgr().getTechHelp(entryId, False, False, False, False, -1)
        return buildLink(gc.getTechInfo, "TXT_KEY_PEDIA_CATEGORY_TECH", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_PROMOTION":
        previewText = CyGameTextMgr().getPromotionHelp(entryId, False)
        return buildLink(gc.getPromotionInfo, "TXT_KEY_PEDIA_CATEGORY_PROMOTION", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_PROJECT":
        previewText = CyGameTextMgr().getProjectHelp(entryId, False, None)
        return buildLink(gc.getProjectInfo, "TXT_KEY_PEDIA_CATEGORY_PROJECT", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_TERRAIN":
        previewText = CyGameTextMgr().getTerrainHelp(entryId, False)
        return buildLink(gc.getTerrainInfo, "TXT_KEY_PEDIA_CATEGORY_TERRAIN", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_FEATURE":
        previewText = CyGameTextMgr().getFeatureHelp(entryId, False)
        return buildLink(gc.getFeatureInfo, "TXT_KEY_PEDIA_CATEGORY_FEATURE", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_BONUS":
        previewText = CyGameTextMgr().getBonusHelp(entryId, False)
        return buildLink(gc.getBonusInfo, "TXT_KEY_PEDIA_CATEGORY_BONUS", entryId), previewText

    elif widgetName == "WIDGET_PEDIA_JUMP_TO_IMPROVEMENT":
        previewText = CyGameTextMgr().getImprovementHelp(entryId, False)
        return buildLink(gc.getImprovementInfo, "TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", entryId), previewText

    # other effects, like map center, trading on ocean, obsolete bonus, reveal bonus
    elif widgetName == "WIDGET_HELP_FOUND_RELIGION":
        TXT_KEY_HELP = "\u01c6First to Discover Founds"
        funcHelp = gc.getReligionInfo
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_OBSOLETE":
        TXT_KEY_HELP = "TXT_KEY_TECH_OBSOLETES"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_IMPROVEMENT":
        TXT_KEY_HELP = "TXT_KEY_MISC_CAN_BUILD_IMPROVEMENT"
        funcHelp = gc.getImprovementInfo
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_BONUS_REVEAL":
        TXT_KEY_HELP = "\u01c6Reveals"
        funcHelp = gc.getBonusInfo
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_IRRIGATION":
        TXT_KEY_HELP = "TXT_KEY_MISC_SPREAD_IRRIGATION"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_IGNORE_IRRIGATION":
        TXT_KEY_HELP = "TXT_KEY_MISC_IRRIGATION_ANYWHERE"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_WORKER_RATE":
        # TODO
        TXT_KEY_HELP = "\u01c6Workers Build Improvements Faster"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_FEATURE_PRODUCTION":
        # TODO
        TXT_KEY_HELP = "\u01c6Workers Produce More Hammers from Chopping"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_MOVE_BONUS":
        # TODO
        TXT_KEY_HELP = "\u01c6Faster Movement on specific Routes"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_BUILD_BRIDGE":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_BRIDGE_BUILDING"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_TERRAIN_TRADE":
        # TODO INTERFACE_TECH_RIVERTRADE, getNumTerrainInfos as item INTERFACE_TECH_RIVERTRADE
        TXT_KEY_HELP = "\u01c6Enables Trade on more Types of Terrain"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_WATER_WORK":
        TXT_KEY_HELP = "TXT_KEY_MISC_WATER_WORK"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_LOS_BONUS":
        TXT_KEY_HELP = "TXT_KEY_UNIT_EXTRA_SIGHT"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_DOMAIN_EXTRA_MOVES":
        # TODO
        TXT_KEY_HELP = "Extra Moves on ..."
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_MAP_CENTER":
        TXT_KEY_HELP = "TXT_KEY_MISC_CENTERS_MAP"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_MAP_REVEAL":
        TXT_KEY_HELP = "TXT_KEY_MISC_REVEALS_MAP"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_MAP_TRADE":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_MAP_TRADING"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_GOLD_TRADE":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_GOLD_TRADING"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_TECH_TRADE":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_TECH_TRADING"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_TRADE_ROUTES":
        TXT_KEY_HELP = "\u01c6+1 Trade Route per City"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_OPEN_BORDERS":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_OPEN_BORDERS"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_DEFENSIVE_PACT":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_DEFENSIVE_PACTS"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_PERMANENT_ALLIANCE":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_PERM_ALLIANCES"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_VASSAL_STATE":
        TXT_KEY_HELP = "TXT_KEY_MISC_ENABLES_VASSAL_STATES"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_HAPPINESS_RATE":
        TXT_KEY_HELP = "\u01c6+1 Happiness in All Cities"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_HEALTH_RATE":
        TXT_KEY_HELP = "\u01c6+1 Health in All Cities"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_ADJUST":
        # item commercetype   Probably TODO
        TXT_KEY_HELP = "TXT_KEY_MISC_ADJUST_COMMERCE_RATE"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_FREE_TECH":
        TXT_KEY_HELP = "TXT_KEY_TECH_FIRST_FREE_TECH"
        funcHelp = None
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText

    elif widgetName == "WIDGET_HELP_FREE_UNIT":
        TXT_KEY_HELP = "TXT_KEY_TECH_FIRST_RECEIVES"
        funcHelp = gc.getUnitInfo
        previewText = buildHelpPreview(TXT_KEY_HELP, funcHelp, HelpEntryId, widgetName, entryId)
        return "", previewText
    
    #   WIDGET_HELP_YIELD_CHANGE # item  # Maybe TODO
    #   WIDGET_HELP_BONUS_PLAYER_TRADE # INTERFACE_TECH_GOLDTRADING # Maybe TODO
    #   WIDGET_HELP_PROCESS_INFO # ?
    
    return "", previewText
