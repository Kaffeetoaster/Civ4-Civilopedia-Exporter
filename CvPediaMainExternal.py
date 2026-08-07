import CvPediaMain
import CvTechChooser
import ScreenExternal
from CvScreenEnums import *

from CvPythonExtensions import *
from Consts import *
from RFCUtils import *

gc = CyGlobalContext()

import time

def logToFile(message, filename="mylog.txt"):
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

def buildLink(categoryName, entryName):
    return "%s#%s" % (categoryName.replace(" ", "-"), entryName.replace(" ", "-"))


def buildPageLink(widgetName, entryId):
    # returns simply something like "Civ#Egypt" or "Tech#Pottery" for the given widgetName and entryId
    if widgetName == "WIDGET_PEDIA_JUMP_TO_CIV":
        entryName = gc.getCivilizationInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_LEADER":
        entryName = gc.getLeaderHeadInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_CIVIC":
        entryName = gc.getCivicInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_RELIGION":
        entryName = gc.getReligionInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_CORPORATIONS":
        entryName = gc.getCorporationInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CORPORATION", ())
        return buildLink(categoryName, entryName)
    elif widgetName in ["WIDGET_PEDIA_JUMP_TO_TECH", "WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH", "WIDGET_PEDIA_JUMP_TO_DERIVED_TECH", "WIDGET_TECH_TREE"]:
        entryName = gc.getTechInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_UNIT":
        entryName = gc.getUnitInfo(entryId).getDescription()
        UnitCategory = getUnitCategory(entryId)
        if UnitCategory == 0:
            categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
        elif UnitCategory == 1:
            categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_MILITARY_UNITS", ())
        elif UnitCategory == 2:
            categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_UNITS", ())

        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_PROMOTION":
        entryName = gc.getPromotionInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_BUILDING":
        entryName = gc.getBuildingInfo(entryId).getDescription()
        buildingCategories = {
            0: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()),
            1: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGIOUS_BUILDINGS", ()),
            2: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIQUE_BUILDINGS", ()),
            3: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_GREAT_PEOPLE_BUILDINGS", ()),
            4: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_NATIONAL_WONDERS", ()),
            5: CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_WORLD_WONDERS", ()),
        }
        categoryName = buildingCategories.get(getBuildingCategory(entryId))
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_PROJECT":
        entryName = gc.getProjectInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_TERRAIN":
        entryName = gc.getTerrainInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_FEATURE":
        entryName = gc.getFeatureInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_BONUS":
        entryName = gc.getBonusInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
        return buildLink(categoryName, entryName)
    elif widgetName == "WIDGET_PEDIA_JUMP_TO_IMPROVEMENT":
        entryName = gc.getImprovementInfo(entryId).getDescription()
        categoryName = CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
        return buildLink(categoryName, entryName)

    else:
        return ""

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
            logToFile("CvPediaMainExternal: %s list length: %d" % (sCategory, len(self.list)), filename="print.txt")
            listasString = ",".join([str(i) for i in self.list])
            logToFile("CvPediaMainExternal: %s list as string: %s" % (sCategory, listasString), filename="print.txt")
            ## end logging
            self.iCategory = iCategory
            func = self.mapScreenFunctions.get(iCategory)
            for i, iItem in enumerate(self.list):
                if iItem[1] != -1: # subcategories like "Ancient Era"  in the Techs have -1 as iItem
        
                    # start new entry for Category in ScreenExternal.CivilopediaData
                    self.screen.CivilopediaData["Categories"][-1]["Entries"].append({"title": iItem[0], "PageContent": []})
                    
                    func.interfaceScreen(iItem[1])
            self.screen.saveCivilopediaDataToFile("CivilopediaData_raw.json")
            
class CvTechChooserExternal(CvTechChooser.CvTechChooser):
    def __init__(self):
        CvTechChooser.CvTechChooser.__init__(self)
        self.techchooser_data = {
            "title": "TechChooser",
            "Techs": [],
            "TechNames": [],
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
        self.screen.saveTechChooserDataToFile("TechChooserData_raw.json")