# Civilopedia Extraction mod module
A small Civ4 BTS mod for extracting and exporting the Civilopedia and Tech Tree infos to json files. To then be used for creating a online version of these resources.



## mod specific changes that are needed
- Each mods needs its own CvPediaMain*External implementation, since the implementation details of the CvPedia Main class is to different across mods.

- previews are created using a CvDLLWidgetData::parseHelp(args) call, which means this function needs to be exposed to python which is it not in most mods.