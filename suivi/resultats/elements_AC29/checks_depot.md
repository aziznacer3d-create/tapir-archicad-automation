# Tests JSON du dépôt, fichier par fichier

290 fichiers lancés sur 292 : 172 entièrement réussis, 118 avec des échecs.
Fichiers mis de côté car Archicad a planté pendant leur test : modify_roof_holes.json, snap_points_hotspots_and_hosted_elements.json

## 3d_window_settings.json

```
AC29 FRA FAIL 22/26 build local tapir 2.0.1
  x Set3DWindowSettings changes the zoom and the pixel size of the 3D window, keeps the values not given and refuses a zero size / read the pixel size / zoom kept: 320 (want ~= 0.5 +/- 1e-06)
  x Set3DWindowSettings changes the zoom and the pixel size of the 3D window, keeps the values not given and refuses a zero size / read the pixel size / zoomDispY kept after the resize: -240 (want ~= -0.25 +/- 1e-06)
  x Set3DWindowSettings changes the zoom and the pixel size of the 3D window, keeps the values not given and refuses a zero size / read the pixel size / zoomScaleX kept after the resize: 6.993757523 (want ~= 0.5 +/- 1e-06)
  x Set3DWindowSettings changes the zoom and the pixel size of the 3D window, keeps the values not given and refuses a zero size / read the pixel size / zoomScaleY kept after the resize: 6.993757523 (want ~= 0.5 +/- 1e-06)
```

## active_graphical_override_combination.json

```
AC29 FRA FAIL 0/0 build local tapir 2.0.1
```

## analytical_load_groups_cases_combinations.json

```
AC29 FRA FAIL 54/57 build local tapir 2.0.1
  x Analytical load groups, load cases and load combinations: create, read back by id, add load cases, delete, and fail on bad input (the template may have load groups of its own, the German one has) / [group, group with an empty name] / empty name: error item in place of the id: null (want exists)
  x Analytical load groups, load cases and load combinations: create, read back by id, add load cases, delete, and fail on bad input (the template may have load groups of its own, the German one has) / [combination with case 1, combination with a load case that does not exist] / nonexistent load case: error item in place of the id: null (want exists)
  x Analytical load groups, load cases and load combinations: create, read back by id, add load cases, delete, and fail on bad input (the template may have load groups of its own, the German one has) / read the combination back by its id, and a combination that does not exist / loadCombinations[0].nationalStandard: null (want == "ENSLSFrequent")
```

## analytical_loads_on_a_beam.json

```
AC29 FRA FAIL 1/4 build local tapir 2.0.1
  x CreateAnalyticalLoads puts a point and an edge load on a beam's curve member, GetAnalyticalLoads reads them back, and both fail on bad input / the beam is a curve member / one curve member: [] (want has 1 items)
  x CreateAnalyticalLoads puts a point and an edge load on a beam's curve member, GetAnalyticalLoads reads them back, and both fail on bad input / the beam is a curve member / of the beam: null (want == "329324EB-406A-46B9-9208-6D0B9C61E711")
  x CreateAnalyticalLoads puts a point and an edge load on a beam's curve member, GetAnalyticalLoads reads them back, and both fail on bad input / the beam's curve / save curve: analyticalMembers[0].curveMember.curve not in answer: {"analyticalMembers": [{"error": {"code": -2130313115, "message": "The element is not
```

## analytical_members_and_releases.json

```
AC29 FRA FAIL 36/44 build local tapir 2.0.1
  x Analytical members: GetAnalyticalMembers lists load-bearing beams and a column, GetAnalyticalMemberDetails, GetAnalyticalMemberPartGeometries and GetLCSOfAnalyticalMembers read their axes, SetAnalyticalReleases replaces a release and refuses a non-member / hinge at the end of the beam / executionResults[0].success: false (want == true)
  x Analytical members: GetAnalyticalMembers lists load-bearing beams and a column, GetAnalyticalMemberDetails, GetAnalyticalMemberPartGeometries and GetLCSOfAnalyticalMembers read their axes, SetAnalyticalReleases replaces a release and refuses a non-member / read the hinge / releases[0].release.releaseDescriptions: [{"ux": "Rigid", "stiffnessX": 0, "uy": "Rigid", "stiffnessY": 0, "uz": "Rigid", "stiffnessZ": 0, "fix": "Rigid", "stiff (want has 1 items)
  x Analytical members: GetAnalyticalMembers lists load-bearing beams and a column, GetAnalyticalMemberDetails, GetAnalyticalMemberPartGeometries and GetLCSOfAnalyticalMembers read their axes, SetAnalyticalReleases replaces a release and refuses a non-member / read the hinge / releases[0].release.releaseDescriptions[0].fiy: "Rigid" (want == "Free")
  x Analytical members: GetAnalyticalMembers lists load-bearing beams and a column, GetAnalyticalMemberDetails, GetAnalyticalMemberPartGeometries and GetLCSOfAnalyticalMembers read their axes, SetAnalyticalReleases replaces a release and refuses a non-member / read the hinge / releases[0].release.releaseDescriptions[0].fiz: "Rigid" (want == "Custom")
  x Analytical members: GetAnalyticalMembers lists load-bearing beams and a column, GetAnalyticalMemberDetails, GetAnalyticalMemberPartGeometries and GetLCSOfAnalyticalMembers read their axes, SetAnalyticalReleases replaces a release and refuses a non-member / read the hinge / releases[0].release.releaseDescriptions[0].stiffnessFiz: 0 (want ~= 500.0 +/- 0.01)
  ... 3 more failures
```

## analytical_members_create_and_types.json

```
AC29 FRA FAIL 10/14 build local tapir 2.0.1
  x CreateElementsFromAnalyticalMembers makes a beam and a column from curve members and refuses incomplete members; GetAnalyticalMemberTypesOfElements names their member types / member types of wall, beam, column and an unknown guid / memberTypesOfElements[0].memberType: "Unknown" (want == "Wall")
  x CreateElementsFromAnalyticalMembers makes a beam and a column from curve members and refuses incomplete members; GetAnalyticalMemberTypesOfElements names their member types / member types of wall, beam, column and an unknown guid / memberTypesOfElements[1].memberType: "Unknown" (want == "Beam")
  x CreateElementsFromAnalyticalMembers makes a beam and a column from curve members and refuses incomplete members; GetAnalyticalMemberTypesOfElements names their member types / member types of wall, beam, column and an unknown guid / memberTypesOfElements[2].memberType: "Unknown" (want == "Column")
  x CreateElementsFromAnalyticalMembers makes a beam and a column from curve members and refuses incomplete members; GetAnalyticalMemberTypesOfElements names their member types / member types of wall, beam, column and an unknown guid / unknown guid is an error item: null (want exists)
```

## analytical_supports_and_links.json

```
AC29 FRA FAIL 6/7 build local tapir 2.0.1
  x CreateAnalyticalSupports and CreateAnalyticalLinks make supports and links on two beams that GetAnalyticalSupports and GetAnalyticalLinks read back, ConvertAnalyticalLinksToNonShortest fixes a shortest link's end, and each refuses a bad element / point support at the start of the first beam, line support along the second, one on a nonexistent member / save s1: elements[0].elementId.guid not in answer: {"error": {"code": -2130312308, "message": "Failed to create the supports."}}
```

## analytical_visibility_settings.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x SetAnalyticalVisibilitySettings changes only the given fields, GetAnalyticalVisibilitySettings reads them back, and an unknown mode is refused / settings before / save loads0: visibilitySettings.loadVisibilityMode not in answer: {"visibilitySettings": {"visibilityMode": "AnalyticalModelWithinEntireModel", "isAnalyt
```

## associative_dimensions_wall_faces.json

```
AC29 FRA FAIL 8/9 build local tapir 2.0.1
  x CreateAssociativeDimensions on wall faces: a perpendicular dimension is created, oblique ones get an error instead of an elementId (#2505) / only that one dimension is in the project / API.GetElementsByType: rejected: {"code": 4002, "message": "Invalid command parameters (The JSON is invalid according to the JSON schema. Validation failed on sche
```

## bounding_boxes_and_model_extent.json

```
AC29 FRA FAIL 20/21 build local tapir 2.0.1
  x Get3DBoundingBoxes, Get2DBoundingBoxes and GetModelExtent measure a wall and a slab, and follow them when they move / model extent covers both / save ezMin: zMin not in answer: {"error": {"code": -2130313110, "message": "Failed to get the model extent"}}
```

## classifications_of_element_defaults.json

```
AC29 FRA FAIL 13/15 build local tapir 2.0.1
  x Classifications of tool defaults: SetClassificationsOfElementDefaults, GetClassificationsOfElementDefaults and GetClassificationsOfToolDefaults / SetClassificationsOfElementDefaults [Wall to T1, Line to T2, Wall to a bogus item, Unknown to T1] / Line to T2: success: false (want == true)
  x Classifications of tool defaults: SetClassificationsOfElementDefaults, GetClassificationsOfElementDefaults and GetClassificationsOfToolDefaults / read the Wall and Line defaults back / save lineDefault: elementDefaultClassifications[1].classificationIds[0].classificationItemId.guid not in answer: {"elementDefaultClassifications": [{"classifi
```

## collisions.json

```
AC29 FRA FAIL 2/8 build local tapir 2.0.1
  x GetCollisions finds a slab cutting through a wall, not a slab apart, and honours the volume tolerance / wall against [crossing slab, slab apart], default-like tolerances / only the crossing slab collides: [] (want has 1 items)
  x GetCollisions finds a slab cutting through a wall, not a slab apart, and honours the volume tolerance / wall against [crossing slab, slab apart], default-like tolerances / collision names the group 1 element: null (want exists)
  x GetCollisions finds a slab cutting through a wall, not a slab apart, and honours the volume tolerance / wall against [crossing slab, slab apart], default-like tolerances / collision names the group 2 element: null (want exists)
  x GetCollisions finds a slab cutting through a wall, not a slab apart, and honours the volume tolerance / wall against [crossing slab, slab apart], default-like tolerances / the bodies intersect: null (want == true)
  x GetCollisions finds a slab cutting through a wall, not a slab apart, and honours the volume tolerance / wall against [crossing slab, slab apart], default-like tolerances / clearance flag under its documented key: null (want exists)
  ... 1 more failures
```

## columns_beams_slabs_create_shared_settings.json

```
AC29 FRA FAIL 2/3 build local tapir 2.0.1
  x CreateColumns, CreateBeams and CreateSlabs take the surfaces, cut fill pens and cover fills that ModifyColumns, ModifyBeams and ModifySlabs write (#2220) / column with cut fill pens and a cover fill / save c1: elements[0].elementId.guid not in answer: {"elements": [{"error": {"code": -2130313112, "message": "No Fill attribute was found for coverFil
```

## copy_library_parts_and_set_picture_images.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x CopyLibraryParts copies a library part into the embedded library and SetLibraryPartPictureImages sets the pictures of the copy (#1950) / library part to copy / save originalFile: fileName not in answer: {"error": {"code": -2130313113, "message": "Not found library part with name 'Model Element' for parentName."}}
```

## create_cameras.json

```
AC29 FRA FAIL 9/30 build local tapir 2.0.1
  x CreateCameras adds cameras to the path of a Camera Set with their positions, two-point perspective, sun and pen (#2657) / GetCameras lists them with what was given / cameraSets[*].cameraSetElementId.guid: null (want contains "93AC26D5-101A-422A-ACF6-355305D7CAB1")
  x CreateCameras adds cameras to the path of a Camera Set with their positions, two-point perspective, sun and pen (#2657) / GetCameras lists them with what was given / cameraSets[*].cameras[*].cameraElementId.guid: null (want contains "5BB8FE16-15DC-4BEF-BE93-096F2203D41B")
  x CreateCameras adds cameras to the path of a Camera Set with their positions, two-point perspective, sun and pen (#2657) / GetCameras lists them with what was given / cameraSets[*].cameras[*].cameraElementId.guid: null (want contains "ED0AF617-F904-4905-975D-96C3B0586D20")
  x CreateCameras adds cameras to the path of a Camera Set with their positions, two-point perspective, sun and pen (#2657) / GetCameras lists them with what was given / camera 1 x: [701.25, 721.5] (want contains 701.25)
  x CreateCameras adds cameras to the path of a Camera Set with their positions, two-point perspective, sun and pen (#2657) / GetCameras lists them with what was given / camera 1 height: [1.75, 2.25] (want contains 1.75)
  ... 16 more failures
```

## create_change_markers.json

```
AC29 FRA FAIL 21/23 build local tapir 2.0.1
  x CreateChangeMarkers creates a Change with its first marker, links a second marker to it, refuses wrong Change links and bad polygons, and GetDetailsOfElements reads the markers back (#2658) / read the markers back / position defaults to the polygon's centre (x): 0 (want ~= 702 +/- 0.001)
  x CreateChangeMarkers creates a Change with its first marker, links a second marker to it, refuses wrong Change links and bad polygons, and GetDetailsOfElements reads the markers back (#2658) / read the markers back / position defaults to the polygon's centre (y): 0 (want ~= 701.5 +/- 0.001)
```

## create_layout_subset.json

```
AC29 FRA FAIL 5/6 build local tapir 2.0.1
  x CreateLayoutSubset answers the id of every subset it creates: without a parent, under a subset and under the Layout Book item (#2627) / subset under the Layout Book item / save subsetC: navigatorItems[0].navigatorItemId.guid not in answer: {"navigatorItems": [{"error": {"code": -2130313112, "message": "Failed to create subse
```

## create_lines_arcs_circles.json

```
AC29 FRA FAIL 39/46 build local tapir 2.0.1
  x CreateLineElements, CreateArcs and CreateCircles keep the geometry, pen, story and layer, and refuse degenerate items (the Element ID is in element_id_on_2d_drafting_elements.json) / read the circles back / detailsOfElements[0].type: "Arc" (want == "Circle")
  x CreateLineElements, CreateArcs and CreateCircles keep the geometry, pen, story and layer, and refuse degenerate items (the Element ID is in element_id_on_2d_drafting_elements.json) / zero-length line / line whose ends coincide refused: null (want exists)
  x CreateLineElements, CreateArcs and CreateCircles keep the geometry, pen, story and layer, and refuse degenerate items (the Element ID is in element_id_on_2d_drafting_elements.json) / arc with zero radius / arc with radius 0 refused: null (want exists)
  x CreateLineElements, CreateArcs and CreateCircles keep the geometry, pen, story and layer, and refuse degenerate items (the Element ID is in element_id_on_2d_drafting_elements.json) / circle with a negative radius / circle with a negative radius refused: null (want exists)
  x CreateLineElements, CreateArcs and CreateCircles keep the geometry, pen, story and layer, and refuse degenerate items (the Element ID is in element_id_on_2d_drafting_elements.json) / only the valid lines were created / elements: [{"elementId": {"guid": "D2FFCC21-FFB1-412F-889E-1C7022DB771F"}}, {"elementId": {"guid": "C0752C09-A4EA-4AA3-A51A-BBF080 (want has 2 items)
  ... 2 more failures
```

## create_modify_camera_sets.json

```
AC29 FRA FAIL 11/16 build local tapir 2.0.1
  x CreateCameraSets creates Camera Sets and ModifyCameraSets renames them and switches the active set (#2657) / set A is the active set / activeCameraSetElementId.guid: null (want == "617AC2E2-8322-4868-8517-F82E8AA0B11E")
  x CreateCameraSets creates Camera Sets and ModifyCameraSets renames them and switches the active set (#2657) / rename set B and make it active / executionResults[0].success: false (want == true)
  x CreateCameraSets creates Camera Sets and ModifyCameraSets renames them and switches the active set (#2657) / set B is now the active set / activeCameraSetElementId.guid: null (want == "B3B5A18E-D4E2-4450-9D70-E9658EABA6A4")
  x CreateCameraSets creates Camera Sets and ModifyCameraSets renames them and switches the active set (#2657) / rename set A only / executionResults[0].success: false (want == true)
  x CreateCameraSets creates Camera Sets and ModifyCameraSets renames them and switches the active set (#2657) / renaming set A kept set B active / activeCameraSetElementId.guid: null (want == "B3B5A18E-D4E2-4450-9D70-E9658EABA6A4")
```

## create_morphs_face_surfaces.json

```
AC29 FRA FAIL 31/32 build local tapir 2.0.1
  x CreateMorphs keeps the surfaces given to the faces of a body, with and without a whole-morph surfaceId (#2626) / the faces have surface B, the whole morphs surface A / morph 2 keeps its whole-morph surface A: 1.0 (want ~= 0 +/- 0.001)
```

## create_profiles_nested_validation.json

```
AC29 FRA FAIL 29/33 build local tapir 2.0.1
  x CreateProfiles refuses unknown keys and unresolved attribute ids inside newSkins, skinOverrides and edgeOverrides (#2585) / C: surfaceId in an edge override (not a ProfileEdgeOverride key) is refused / failed: null (want exists)
  x CreateProfiles refuses unknown keys and unresolved attribute ids inside newSkins, skinOverrides and edgeOverrides (#2585) / C: surfaceId in an edge override (not a ProfileEdgeOverride key) is refused / the error names the key: null (want contains "surfaceId")
  x CreateProfiles refuses unknown keys and unresolved attribute ids inside newSkins, skinOverrides and edgeOverrides (#2585) / C: surfaceId in an edge override (not a ProfileEdgeOverride key) is refused / the error names the path: null (want contains "#/profileDataArray/0/newSkins/0/edgeOverrides/0")
  x CreateProfiles refuses unknown keys and unresolved attribute ids inside newSkins, skinOverrides and edgeOverrides (#2585) / C: surfaceId in an edge override (not a ProfileEdgeOverride key) is refused / nothing created: {"guid": "A82E0ABD-91A9-495E-9EF6-A48F4E62CD91"} (want missing)
```

## create_railings_curtain_walls.json

```
AC29 FRA FAIL 58/65 build local tapir 2.0.1
  x CreateRailings and CreateCurtainWalls keep the reference line, heights, story, pattern and id, and refuse bad items / subelements of the curtain walls / 3 + 2 columns of 1 m times 2 rows of 1 m give 10 panels: [{"elementId": {"guid": "4EF5DD1F-5824-45BD-8B73-7866D0C0CA78"}}, {"elementId": {"guid": "ED4FDE5D-BE7F-42B7-9977-4B1857 (want has 10 items)
  x CreateRailings and CreateCurtainWalls keep the reference line, heights, story, pattern and id, and refuse bad items / read the segments back / first segment begins at the first coordinate (y): 699.94 (want ~= 700.0 +/- 0.001)
  x CreateRailings and CreateCurtainWalls keep the reference line, heights, story, pattern and id, and refuse bad items / read the segments back / first segment ends at the second coordinate (x): 953.06 (want ~= 953.0 +/- 0.001)
  x CreateRailings and CreateCurtainWalls keep the reference line, heights, story, pattern and id, and refuse bad items / read the segments back / first segment ends at the second coordinate (y): 699.94 (want ~= 700.0 +/- 0.001)
  x CreateRailings and CreateCurtainWalls keep the reference line, heights, story, pattern and id, and refuse bad items / read the segments back / second segment begins at the second coordinate (x): 953.06 (want ~= 953.0 +/- 0.001)
  ... 2 more failures
```

## create_skylights_in_roofs.json

```
AC29 FRA FAIL 9/10 build local tapir 2.0.1
  x CreateSkylights places skylights in single- and multi-plane roofs and refuses other owners / placement on the roof slopes / multi-plane skylights have different surface normals: 0.0 (want > 0.1)
```

## create_windows_doors_id_and_layer.json

```
AC29 FRA FAIL 9/11 build local tapir 2.0.1
  x CreateWindows and CreateDoors set the given id and layerIndex, and refuse a nonexistent layer (#2576) / read the window and the door back / window layerIndex applied: 2 (want == 12)
  x CreateWindows and CreateDoors set the given id and layerIndex, and refuse a nonexistent layer (#2576) / read the window and the door back / door layerIndex applied: 2 (want == 12)
```

## create_windows_doors_keep_marker.json

```
AC29 FRA FAIL 2/4 build local tapir 2.0.1
  x CreateWindows and CreateDoors still place the tool's marker when it can be read / markers / window has its marker: null (want exists)
  x CreateWindows and CreateDoors still place the tool's marker when it can be read / markers / door has its marker: null (want exists)
```

## curtain_walls_modify.json

```
AC29 FRA FAIL 65/85 build local tapir 2.0.1
  x ModifyCurtainWalls and ModifyCurtainWallFrames: every change read back, bad inputs refused / subelements as created / A has 4 + 2 columns of 1.5 m and 2 rows of 1.5 m: [{"elementId": {"guid": "F1042BE2-4A07-496C-9189-73668D453006"}}, {"elementId": {"guid": "90AB5300-B5F9-4EE6-AB72-4BC7F7 (want has 12 items)
  x ModifyCurtainWalls and ModifyCurtainWallFrames: every change read back, bad inputs refused / ModifyCurtainWalls: height only / height change accepted: false (want == true)
  x ModifyCurtainWalls and ModifyCurtainWallFrames: every change read back, bad inputs refused / A after the height change / height changed: 3 (want ~= 4.5 +/- 0.001)
  x ModifyCurtainWalls and ModifyCurtainWallFrames: every change read back, bad inputs refused / A after the height change / actual height changed: 3 (want ~= 4.5 +/- 0.001)
  x ModifyCurtainWalls and ModifyCurtainWallFrames: every change read back, bad inputs refused / A details after the bottom change / height unchanged: 3 (want ~= 4.5 +/- 0.001)
  ... 15 more failures
```

## delete_and_replace_layers.json

```
AC29 FRA FAIL 13/22 build local tapir 2.0.1
  x DeleteAndReplaceAttributes moves the elements of a layer to a locked replacement layer, deletes the layer, keeps the replacement locked and changes nothing with dryRun (#2829) / replace layer A by B, dry run / no error: {"code": -2130313110, "message": "Failed to read the elements of every view and layout, so the layer was not deleted."} (want missing)
  x DeleteAndReplaceAttributes moves the elements of a layer to a locked replacement layer, deletes the layer, keeps the replacement locked and changes nothing with dryRun (#2829) / replace layer A by B, dry run / would delete A: null (want == true)
  x DeleteAndReplaceAttributes moves the elements of a layer to a locked replacement layer, deletes the layer, keeps the replacement locked and changes nothing with dryRun (#2829) / replace layer A by B, dry run / lists the wall: null (want has 1 items)
  x DeleteAndReplaceAttributes moves the elements of a layer to a locked replacement layer, deletes the layer, keeps the replacement locked and changes nothing with dryRun (#2829) / replace layer A by B, dry run / the wall: null (want == "673D9B37-277A-4C96-81D8-A038BA8DDBA5")
  x DeleteAndReplaceAttributes moves the elements of a layer to a locked replacement layer, deletes the layer, keeps the replacement locked and changes nothing with dryRun (#2829) / replace layer A by B, dry run / lists the views to rebuild: null (want exists)
  ... 4 more failures
```

## delete_and_replace_profiles_zone_categories.json

```
AC29 FRA FAIL 23/30 build local tapir 2.0.1
  x DeleteAndReplaceAttributes replaces a profile in a profiled column and a zone category in a zone (#2829) / replace profile A by B, dry run / lists the column: [] (want has 1 items)
  x DeleteAndReplaceAttributes replaces a profile in a profiled column and a zone category in a zone (#2829) / replace profile A by B, dry run / the column: null (want == "526B5EDF-A4B5-4A09-9274-A0CA4C133910")
  x DeleteAndReplaceAttributes replaces a profile in a profiled column and a zone category in a zone (#2829) / the column still uses A after the dry run / profile A: "00000000-0000-0000-0000-000000000000" (want == "39DE6BC5-F908-4393-AFAF-5281EE59C335")
  x DeleteAndReplaceAttributes replaces a profile in a profiled column and a zone category in a zone (#2829) / replace profile A by B / rewrote the column: [] (want has 1 items)
  x DeleteAndReplaceAttributes replaces a profile in a profiled column and a zone category in a zone (#2829) / replace profile A by B / no warnings: ["A view or layout database could not be opened, so its elements were not checked.", "A view or layout database could no (want missing)
  ... 2 more failures
```

## design_option_combinations_and_views.json

```
AC29 FRA FAIL 37/42 build local tapir 2.0.1
  x Design option combinations: create, set, activate, deactivate, rename, duplicate and delete them, and set the combination of a view / read the sets / designOptionSets[0].name: "TapirCheck set B" (want == "TapirCheck set A")
  x Design option combinations: create, set, activate, deactivate, rename, duplicate and delete them, and set the combination of a view / read the sets / designOptionSets[0].designOptions: [{"designOptionId": {"guid": "1D5875E8-7827-48F4-A70A-D3A1CED41CD4"}}] (want has 2 items)
  x Design option combinations: create, set, activate, deactivate, rename, duplicate and delete them, and set the combination of a view / read the sets / designOptionSets[1].name: "TapirCheck set A" (want == "TapirCheck set B")
  x Design option combinations: create, set, activate, deactivate, rename, duplicate and delete them, and set the combination of a view / read the sets / designOptionSets[1].designOptions: [{"designOptionId": {"guid": "E25B1DCC-F1DB-4A53-953A-FFE402A1546D"}}, {"designOptionId": {"guid": "05465407-B123-43C4-A (want has 1 items)
  x Design option combinations: create, set, activate, deactivate, rename, duplicate and delete them, and set the combination of a view / Project Map story / navigatorItemTree.children[0].navigatorItem.children[0].navigatorItem.type: "UndefinedItem" (want == "StoryItem")
```

## detail_marker_pens_and_angle.json

```
AC29 FRA FAIL 10/12 build local tapir 2.0.1
  x ModifyDetailMarkers writes the boundary pen and line type, the marker angle, always-horizontal and the marker symbol's pen of Detail and Worksheet markers (#2230) / pens, line type, angle and a turning marker on the detail marker / applied (read back by the command): false (want == true)
  x ModifyDetailMarkers writes the boundary pen and line type, the marker angle, always-horizontal and the marker symbol's pen of Detail and Worksheet markers (#2230) / an always horizontal marker and another pen on the worksheet marker / applied (read back by the command): false (want == true)
```

## details_and_worksheets_databases.json

```
AC29 FRA FAIL 22/28 build local tapir 2.0.1
  x CreateDetails and CreateWorksheets make databases that GetDatabases lists and GetDatabaseIdFromNavigatorItemId resolves / the worksheet is listed with its name and ID / databases: [{"type": "Worksheet", "databaseId": {"guid": "2830805D-E793-1942-995B-B7A390E849F5"}, "name": "Cartouche 02", "referenc (want has 1 items)
  x CreateDetails and CreateWorksheets make databases that GetDatabases lists and GetDatabaseIdFromNavigatorItemId resolves / the worksheet is listed with its name and ID / databases[0].name: "Cartouche 02" (want == "TapirCheck Worksheet")
  x CreateDetails and CreateWorksheets make databases that GetDatabases lists and GetDatabaseIdFromNavigatorItemId resolves / the worksheet is listed with its name and ID / databases[0].referenceId: "Z-02" (want == "TCW-1")
  x CreateDetails and CreateWorksheets make databases that GetDatabases lists and GetDatabaseIdFromNavigatorItemId resolves / types in the given order, a repeated type once / databases: [{"type": "Worksheet", "databaseId": {"guid": "2830805D-E793-1942-995B-B7A390E849F5"}, "name": "Cartouche 02", "referenc (want has 2 items)
  x CreateDetails and CreateWorksheets make databases that GetDatabases lists and GetDatabaseIdFromNavigatorItemId resolves / types in the given order, a repeated type once / databases[1].type: "Worksheet" (want == "Detail")
  ... 1 more failures
```

## dimension_witness_point_texts.json

```
AC29 FRA FAIL 22/25 build local tapir 2.0.1
  x Linear dimensions: custom text, superscript and text position per witness point, written by ModifyAssociativeDimensions and read back by GetDimensionData (#2663 part 4) / custom texts, superscript and a reset position / texts accepted and read back by the command: false (want == true)
  x Linear dimensions: custom text, superscript and text position per witness point, written by ModifyAssociativeDimensions and read back by GetDimensionData (#2663 part 4) / the texts read back / measured value placeholder round-trips: "400 ok" (want == "{MeasuredValue} ok")
  x Linear dimensions: custom text, superscript and text position per witness point, written by ModifyAssociativeDimensions and read back by GetDimensionData (#2663 part 4) / the texts after the second change / third text unchanged: "400 ok" (want == "{MeasuredValue} ok")
```

## dimensions_details_panel.json

```
AC29 FRA FAIL 22/27 build local tapir 2.0.1
  x Linear dimensions: opening heights in the chain and the layered element options written and read back (#2663 part 5) / the dimensions read back / core on: false (want == true)
  x Linear dimensions: opening heights in the chain and the layered element options written and read back (#2663 part 5) / the dimensions read back / second: total off: true (want == false)
  x Linear dimensions: opening heights in the chain and the layered element options written and read back (#2663 part 5) / the dimensions read back / second: reference line on: false (want == true)
  x Linear dimensions: opening heights in the chain and the layered element options written and read back (#2663 part 5) / GetDimensionData returns the details panel / core in GetDimensionData: false (want == true)
  x Linear dimensions: opening heights in the chain and the layered element options written and read back (#2663 part 5) / the details panel after the change / second: reference line kept: false (want == true)
```

## dimensions_layer_static_only_text.json

```
AC29 FRA FAIL 18/22 build local tapir 2.0.1
  x Linear dimensions: layerIndex on creation, staticDimension and onlyDimensionText written and read back (#2663 part 1) / the dimensions read back / second not static: true (want == false)
  x Linear dimensions: layerIndex on creation, staticDimension and onlyDimensionText written and read back (#2663 part 1) / ModifyAssociativeDimensions switches both checkboxes / first change accepted: false (want == true)
  x Linear dimensions: layerIndex on creation, staticDimension and onlyDimensionText written and read back (#2663 part 1) / the checkboxes after the change / static off: true (want == false)
  x Linear dimensions: layerIndex on creation, staticDimension and onlyDimensionText written and read back (#2663 part 1) / the checkboxes after the change / second static unchanged: true (want == false)
```

## drawing_pens_colors_and_anchor.json

```
AC29 FRA FAIL 1/3 build local tapir 2.0.1
  x SetDetailsOfElements writes a Drawing's pen table, color mode, transparent background and anchor, CreateDrawings places a Drawing by a given anchorPoint, and GetDetailsOfElements reads them back with offset (#2230, #2511) / subset second in the Layout Book / success: false (want == true)
  x SetDetailsOfElements writes a Drawing's pen table, color mode, transparent background and anchor, CreateDrawings places a Drawing by a given anchorPoint, and GetDetailsOfElements reads them back with offset (#2230, #2511) / the layout in the Layout Book / save layout: navigatorItemTree.children[1].navigatorItem.children[0].navigatorItem.navigatorItemId.guid not in answer: {"navigatorItemTree": {"type": "Un
```

## drawing_primitives_text_content.json

```
AC29 FRA FAIL 6/7 build local tapir 2.0.1
  x GetDrawingPrimitivesOfElements and GetShapePrimitivesOfElements return the content of text primitives, also of a zone stamp (#2803) / drawing primitives with text content / the zone's drawing has the texts of its stamp: null (want exists)
```

## electrical_panels_devices_circuits.json

```
AC29 FRA FAIL 0/0 build local tapir 2.0.1
```

## electrical_project_settings.json

```
AC29 FRA FAIL 0/0 build local tapir 2.0.1
```

## element_groups.json

```
AC29 FRA FAIL 61/66 build local tapir 2.0.1
  x Groups: create nested groups, read them back, store user data on them and ungroup them; Suspend Groups and Auto Group modes / the group of w1 is the inner group, the group of w3 the outer one / group of w3: inner group, w3 and w4: [{"elementId": {"guid": "4C9C19BE-9317-4AF7-846C-4AEEB687438D"}}, {"elementId": {"guid": "97749043-F282-4D6E-85FA-5F9058 (want has 3 items)
  x Groups: create nested groups, read them back, store user data on them and ungroup them; Suspend Groups and Auto Group modes / direct elements of the groups / outer: inner group, w3 and w4: [{"elementId": {"guid": "4C9C19BE-9317-4AF7-846C-4AEEB687438D"}}, {"elementId": {"guid": "97749043-F282-4D6E-85FA-5F9058 (want has 3 items)
  x Groups: create nested groups, read them back, store user data on them and ungroup them; Suspend Groups and Auto Group modes / the top level group of both is the outer group / top level of inner is outer: [{"elementId": {"guid": "4C9C19BE-9317-4AF7-846C-4AEEB687438D"}}, {"elementId": {"guid": "97749043-F282-4D6E-85FA-5F9058 (want has 3 items)
  x Groups: create nested groups, read them back, store user data on them and ungroup them; Suspend Groups and Auto Group modes / the top level group of both is the outer group / top level of outer is itself: [{"elementId": {"guid": "4C9C19BE-9317-4AF7-846C-4AEEB687438D"}}, {"elementId": {"guid": "97749043-F282-4D6E-85FA-5F9058 (want has 3 items)
  x Groups: create nested groups, read them back, store user data on them and ungroup them; Suspend Groups and Auto Group modes / nothing was ungrouped / elementsOfGroups[1].elements: [{"elementId": {"guid": "4C9C19BE-9317-4AF7-846C-4AEEB687438D"}}, {"elementId": {"guid": "97749043-F282-4D6E-85FA-5F9058 (want has 3 items)
```

## element_id_on_2d_drafting_elements.json

```
AC29 FRA FAIL 17/24 build local tapir 2.0.1
  x Lines, arcs, circles, polylines, splines and hotspots have no Element ID on Archicad 29 and later: an id is refused with APIERR_BADELEMENTTYPE and creates or changes nothing (#2762) / line with an id / line id refused as APIERR_BADELEMENTTYPE: -2130312311 (want == -2130313103)
  x Lines, arcs, circles, polylines, splines and hotspots have no Element ID on Archicad 29 and later: an id is refused with APIERR_BADELEMENTTYPE and creates or changes nothing (#2762) / arc with an id / arc id refused as APIERR_BADELEMENTTYPE: -2130312311 (want == -2130313103)
  x Lines, arcs, circles, polylines, splines and hotspots have no Element ID on Archicad 29 and later: an id is refused with APIERR_BADELEMENTTYPE and creates or changes nothing (#2762) / circle with an id / circle id refused as APIERR_BADELEMENTTYPE: -2130312311 (want == -2130313103)
  x Lines, arcs, circles, polylines, splines and hotspots have no Element ID on Archicad 29 and later: an id is refused with APIERR_BADELEMENTTYPE and creates or changes nothing (#2762) / polyline with an id / polyline id refused as APIERR_BADELEMENTTYPE: -2130312311 (want == -2130313103)
  x Lines, arcs, circles, polylines, splines and hotspots have no Element ID on Archicad 29 and later: an id is refused with APIERR_BADELEMENTTYPE and creates or changes nothing (#2762) / spline with an id / spline id refused as APIERR_BADELEMENTTYPE: -2130312311 (want == -2130313103)
  ... 2 more failures
```

## element_quantities.json

```
AC29 FRA FAIL 41/42 build local tapir 2.0.1
  x GetQuantitiesOfElements and GetSurfaceQuantitiesOfElements calculate a wall, a slab with a hole and a zone / wall A with minOpeningSize 2 m2: the 1.2 m2 window is not subtracted from the conditional surface (the DevKit names the wall's surface, not its volume) / conditional surface grows by the window: 0.0 (want > 0.5)
```

## favorite_folders.json

```
AC29 FRA FAIL 49/50 build local tapir 2.0.1
  x Favorite folders: CreateFavoriteFolder, RenameFavoriteFolder, MoveFavorites, MoveFavoriteFolder, DeleteFavoriteFolder, GetFavoriteFolders and GetAllFavorites change and read the Favorites palette and refuse bad paths / spline favorites / only the new spline favorite (the templates have none): [{"name": "Tapir check folder spline favorite", "elementType": "Spline"}, {"name": "00 - Spline (d\u00e9faut)", "element (want has 1 items)
```

## favorites_from_elements.json

```
AC29 FRA FAIL 46/48 build local tapir 2.0.1
  x Favorites from elements: CreateFavoritesFromElements, GetFavoritesByType, GetFavoriteDetails, GetFavoriteSettings, UpdateFavoritesFromElements, ApplyFavoritesToElements, RenameFavorites and DeleteFavorites change what they say and fail per item on bad input / spline favorites / only the new spline favorite (the templates have none): ["Tapir check spline favorite", "00 - Spline (d\u00e9faut)"] (want has 1 items)
  x Favorites from elements: CreateFavoritesFromElements, GetFavoritesByType, GetFavoriteDetails, GetFavoriteSettings, UpdateFavoritesFromElements, ApplyFavoritesToElements, RenameFavorites and DeleteFavorites change what they say and fail per item on bad input / no spline favorite left / favorites: ["00 - Spline (d\u00e9faut)"] (want has 0 items)
```

## gdl_parameter_script_sets_back.json

```
AC29 FRA FAIL 10/14 build local tapir 2.0.1
  x SetGDLParametersOfElements reports a written parameter that the object's Parameter Script sets back, and still writes the other given parameters (#2396) / read back / third parameter is tapirFixed: "ZZYZX" (want == "tapirFixed")
  x SetGDLParametersOfElements reports a written parameter that the object's Parameter Script sets back, and still writes the other given parameters (#2396) / read back / tapirFixed is what the script sets: 0.5 (want == "fixed")
  x SetGDLParametersOfElements reports a written parameter that the object's Parameter Script sets back, and still writes the other given parameters (#2396) / read back / fourth parameter is tapirFree: "AC_show2DHotspotsIn3D" (want == "tapirFree")
  x SetGDLParametersOfElements reports a written parameter that the object's Parameter Script sets back, and still writes the other given parameters (#2396) / read back / the other given parameter was written: true (want == "three")
```

## get_all_elements_skips_subelement_objects.json

```
AC29 FRA FAIL 3/6 build local tapir 2.0.1
  x GetAllElements and GetElementsByType leave out zone stamps unless IncludeSubElemObjects is given / all elements on story 1 / only the zone, not its stamp: [{"elementId": {"guid": "0B29C8F4-3556-7E44-AD71-2A2297C232AB"}}, {"elementId": {"guid": "19AD82A2-E1F7-45BA-B9DA-660187 (want has 1 items)
  x GetAllElements and GetElementsByType leave out zone stamps unless IncludeSubElemObjects is given / all elements on story 1 with sub-element objects / the zone and its stamp: [{"elementId": {"guid": "4B0A3EA1-17FD-4857-A9FB-8DC72A978922"}}, {"elementId": {"guid": "2FFC83E4-A07A-4F6F-ABAB-1A691D (want has 2 items)
  x GetAllElements and GetElementsByType leave out zone stamps unless IncludeSubElemObjects is given / objects on story 1 with sub-element objects / the stamp on request: [{"elementId": {"guid": "4B0A3EA1-17FD-4857-A9FB-8DC72A978922"}}, {"elementId": {"guid": "2FFC83E4-A07A-4F6F-ABAB-1A691D (want has 1 items)
```

## get_details_of_railing_components.json

```
AC29 FRA FAIL 1/2 build local tapir 2.0.1
  x GetDetailsOfElements reads a post, the top rail and the pattern of a railing, with their owners (#2572) / components of the railing / save pattern: subelements[0].railingPatterns[0].elementId.guid not in answer: {"subelements": [{"railingNodes": [{"elementId": {"guid": "1DDAC7EC-7C2E-4C1
```

## get_elements_in_draw_order_resolvable.json

```
AC29 FRA FAIL 3/4 build local tapir 2.0.1
  x GetElementsInDrawOrder returns only elements the other commands can find by guid (#2492) / every listed guid resolves / no listed guid answers 'Element not found': null (want exists)
```

## get_profile_values_of_elements.json

```
AC29 FRA FAIL 1/2 build local tapir 2.0.1
  x GetProfileValuesOfElements reads the stretched profile of a Profile wall and of each Profile segment of a beam (#2587) / a Profile wall / save pw: elements[0].elementId.guid not in answer: {"elements": [{"error": {"code": -2130313112, "message": "Invalid attribute reference in 'profileI
```

## graphic_override_read_criterion_layers_construction.json

```
AC29 FRA FAIL 1/8 build local tapir 2.0.1
  x Graphic override rules: includeCriterion reads the Layers, Model View and Construction conditions by name / read criterion / layer by name: null (want == "TapirCheck read criterion layer")
  x Graphic override rules: includeCriterion reads the Layers, Model View and Construction conditions by name / read criterion / layer name starts with: null (want == "Tapir & Co")
  x Graphic override rules: includeCriterion reads the Layers, Model View and Construction conditions by name / read criterion / layer not locked: null (want == false)
  x Graphic override rules: includeCriterion reads the Layers, Model View and Construction conditions by name / read criterion / composite name contains: null (want == "Brick")
  x Graphic override rules: includeCriterion reads the Layers, Model View and Construction conditions by name / read criterion / structure type: null (want == "Composite")
  ... 2 more failures
```

## graphic_override_rule_groups_order_and_move.json

```
AC29 FRA FAIL 28/55 build local tapir 2.0.1
  x Graphic override rule groups: create, order, rename; rules: order, move, find by name, delete / groups A, B first / success: false (want == true)
  x Graphic override rule groups: create, order, rename; rules: order, move, find by name, delete / read A, B / graphicOverrideRuleGroups[0].name: "R\u00e9novation" (want == "TapirCheck group A")
  x Graphic override rule groups: create, order, rename; rules: order, move, find by name, delete / read A, B / graphicOverrideRuleGroups[1].name: "R\u00e8gles de Substitutions graphiques" (want == "TapirCheck group B")
  x Graphic override rule groups: create, order, rename; rules: order, move, find by name, delete / read A, B / empty group listed: [{"graphicOverrideRuleId": {"guid": "5AB0C94A-E9EF-4F00-BB8C-6D33C589896A"}}, {"graphicOverrideRuleId": {"guid": "6702CC (want has 0 items)
  x Graphic override rule groups: create, order, rename; rules: order, move, find by name, delete / B first, the others follow / success: false (want == true)
  ... 22 more failures
```

## graphical_override_rule_and_combination.json

```
AC29 FRA FAIL 31/33 build local tapir 2.0.1
  x CreateGraphicalOverrideRule and CreateGraphicalOverrideCombination create and overwrite by name; combinations are renamed and listed; the style of elements is read / read the rule / graphicOverrideRules[0].style.surfaceColor.green: 0.498039216 (want ~= 0.5 +/- 0.001)
  x CreateGraphicalOverrideRule and CreateGraphicalOverrideCombination create and overwrite by name; combinations are renamed and listed; the style of elements is read / read the rule / graphicOverrideRules[0].style.surfaceColor.blue: 0.247058824 (want ~= 0.25 +/- 0.001)
```

## issues_create_comment_attach_delete.json

```
AC29 FRA FAIL 36/38 build local tapir 2.0.1
  x Issues: CreateIssue, AddCommentToIssue, AttachElementsToIssue, DetachElementsFromIssue and DeleteIssue change what GetIssues, GetCommentsFromIssue and GetElementsAttachedToIssue read back / read the Modification elements / wall 2 only: [{"elementId": {"guid": "09E5881B-1AA5-46F5-B0B8-6344937042F8"}}, {"elementId": {"guid": "9BB2DDE5-981F-4D34-A897-15FE38 (want has 1 items)
  x Issues: CreateIssue, AddCommentToIssue, AttachElementsToIssue, DetachElementsFromIssue and DeleteIssue change what GetIssues, GetCommentsFromIssue and GetElementsAttachedToIssue read back / Modification elements after the detach / wall 2 still attached: [{"elementId": {"guid": "09E5881B-1AA5-46F5-B0B8-6344937042F8"}}, {"elementId": {"guid": "9BB2DDE5-981F-4D34-A897-15FE38 (want has 1 items)
```

## keynotes_create_modify_delete_label.json

```
AC29 FRA FAIL 70/72 build local tapir 2.0.1
  x Keynote folders and items: create, read back, modify, label and delete (#1938) / [autotexts of item 1, of a missing item] / missing item: error: null (want exists)
  x Keynote folders and items: create, read back, modify, label and delete (#1938) / [label of a missing item] / missing item: error: null (want exists)
```

## labels_layer_and_move.json

```
AC29 FRA FAIL 19/26 build local tapir 2.0.1
  x CreateLabels puts the label on the given layerIndex and refuses a missing layer; ModifyLabels moves and re-points a label with begCoordinate, midCoordinate and endCoordinate (#2666) / read the moved labels / label 1 mid x moved: 809 (want ~= 806.0 +/- 0.001)
  x CreateLabels puts the label on the given layerIndex and refuses a missing layer; ModifyLabels moves and re-points a label with begCoordinate, midCoordinate and endCoordinate (#2666) / read the moved labels / label 1 mid y moved: 814 (want ~= 812.0 +/- 0.001)
  x CreateLabels puts the label on the given layerIndex and refuses a missing layer; ModifyLabels moves and re-points a label with begCoordinate, midCoordinate and endCoordinate (#2666) / read the moved labels / label 1 end x moved: 811 (want ~= 808.0 +/- 0.001)
  x CreateLabels puts the label on the given layerIndex and refuses a missing layer; ModifyLabels moves and re-points a label with begCoordinate, midCoordinate and endCoordinate (#2666) / read the moved labels / label 1 end y moved: 814 (want ~= 812.0 +/- 0.001)
  x CreateLabels puts the label on the given layerIndex and refuses a missing layer; ModifyLabels moves and re-points a label with begCoordinate, midCoordinate and endCoordinate (#2666) / read the moved labels / label 2 mid kept: 820 (want ~= 821.0 +/- 0.001)
  ... 2 more failures
```

## layout_book_drawings.json

```
AC29 FRA FAIL 6/8 build local tapir 2.0.1
  x Layout Book drawings: CreateDrawings, GetDrawingContentBoxes, UpdateDrawings and ChangeDrawingLink place, read, update and relink a Drawing, and refuse bad input / subset second in the Layout Book / success: false (want == true)
  x Layout Book drawings: CreateDrawings, GetDrawingContentBoxes, UpdateDrawings and ChangeDrawingLink place, read, update and relink a Drawing, and refuse bad input / the Drawing is on the layout / save layout: navigatorItemTree.children[1].navigatorItem.children[0].navigatorItem.navigatorItemId.guid not in answer: {"navigatorItemTree": {"type": "Un
```

## layout_book_layouts_and_subsets.json

```
AC29 FRA FAIL 26/29 build local tapir 2.0.1
  x Layout Book: CreateLayoutSubset, CreateLayout, GetLayoutSubsetSettings, GetLayoutSettings and SetLayoutSettings write what they say, and refuse bad input / subset second in the Layout Book / success: false (want == true)
  x Layout Book: CreateLayoutSubset, CreateLayout, GetLayoutSubsetSettings, GetLayoutSettings and SetLayoutSettings write what they say, and refuse bad input / read layout one / layoutSettings[0].layoutName: "TCL007 Tapir check layout one" (want == "Tapir check layout one")
  x Layout Book: CreateLayoutSubset, CreateLayout, GetLayoutSubsetSettings, GetLayoutSettings and SetLayoutSettings write what they say, and refuse bad input / layout one is the only item of the subset / save layout1: navigatorItemTree.children[1].navigatorItem.children[0].navigatorItem.navigatorItemId.guid not in answer: {"navigatorItemTree": {"type": "Un
```

## level_dimensions_static_and_owner.json

```
AC29 FRA FAIL 21/24 build local tapir 2.0.1
  x ModifyLevelDimensions: the value of a static level dimension, the Static checkbox and the owner element, read back by GetDetailsOfElements (#2656) / ModifyLevelDimensions: Static on for the associative one / Static on accepted: false (want == true)
  x ModifyLevelDimensions: the value of a static level dimension, the Static checkbox and the owner element, read back by GetDetailsOfElements (#2656) / after Static on / static: false (want == true)
  x ModifyLevelDimensions: the value of a static level dimension, the Static checkbox and the owner element, read back by GetDetailsOfElements (#2656) / after Static on / keeps the upper slab's height: -110000000 (want ~= 2.4 +/- 0.5)
```

## level_dimensions_text_content.json

```
AC29 FRA FAIL 13/17 build local tapir 2.0.1
  x CreateLevelDimensions and ModifyLevelDimensions: measured or custom text content of both texts, read back by GetDetailsOfElements (#2656) / ModifyLevelDimensions: another custom text and a custom second text / text change accepted: false (want == true)
  x CreateLevelDimensions and ModifyLevelDimensions: measured or custom text content of both texts, read back by GetDetailsOfElements (#2656) / texts after the change / second text custom: "Measured" (want == "Custom")
  x CreateLevelDimensions and ModifyLevelDimensions: measured or custom text content of both texts, read back by GetDetailsOfElements (#2656) / texts after the change / second custom text: null (want == "T2656")
  x CreateLevelDimensions and ModifyLevelDimensions: measured or custom text content of both texts, read back by GetDetailsOfElements (#2656) / measured content after the change / second text left as it was: "Measured" (want == "Custom")
```

## level_dimensions_text_style.json

```
AC29 FRA FAIL 16/20 build local tapir 2.0.1
  x CreateLevelDimensions and ModifyLevelDimensions: text font and bold/italic/underline, read back by GetDetailsOfElements (#2656) / read the text style back / font as created: "Arial Occidental" (want == "Arial")
  x CreateLevelDimensions and ModifyLevelDimensions: text font and bold/italic/underline, read back by GetDetailsOfElements (#2656) / style after the change / font kept: "Arial Occidental" (want == "Arial")
  x CreateLevelDimensions and ModifyLevelDimensions: text font and bold/italic/underline, read back by GetDetailsOfElements (#2656) / font after the change by index / same font by index: "Arial Occidental" (want == "Arial")
  x CreateLevelDimensions and ModifyLevelDimensions: text font and bold/italic/underline, read back by GetDetailsOfElements (#2656) / the refused item changed nothing / font unchanged: "Arial Occidental" (want == "Arial")
```

## library_part_editing.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x Library part editing: parameters, scripts, metadata, custom sections, pictures and CreateLibraryPart / [edit, subtype, locked] / save subIdx: libraryParts[1].index not in answer: {"libraryParts": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Model E
```

## library_part_from_elements_2d_and_3d.json

```
AC29 FRA FAIL 1/2 build local tapir 2.0.1
  x CreateLibraryPartFromElements makes an object of a drawn circle, GetLibraryPart2DPrimitives reads its symbol back and InterpretGDLScript3D runs its 3D script (#1950) / library part of the circle / save partName: name not in answer: {"error": {"code": -2130313113, "message": "Not found library part with name 'Model Element' for parentName."}}
```

## library_part_sections.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x CreateLibraryParts, GetLibraryPartSections, GetLibraryPartSection and UpdateLibraryPartSections on a new library part / [part, no parent, unknown parent GUID] / save idx: libraryParts[0].index not in answer: {"libraryParts": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Model E
```

## library_parts_find_and_inspect.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x Finding and inspecting library parts: a parent and a child part of the embedded library through the library part commands of the classic API / parent part under the Model Element (by name) / save parentUnId: libraryParts[0].unId not in answer: {"libraryParts": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Model El
```

## library_parts_library_manager.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x Finding and inspecting library parts with the Library Manager: FindLibraryParts, GetLibraryPartDetails and GetLibraryPartFileInfo on a parent and a child part of the embedded library / parent part under the Model Element (by name) / save parentUnId: libraryParts[0].unId not in answer: {"libraryParts": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Model El
```

## library_parts_library_of_part.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x GetLibrariesOfLibParts finds the embedded library of a new library part by file name and by guid / part in the embedded library / save partGuid: libraryParts[0].guid not in answer: {"libraryParts": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Model El
```

## library_parts_missing_part_name.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x GetMissingLibPartNames names the library part of a placed object, also after the part was removed from the libraries / part in the embedded library / save partPath: libraryParts[0].path not in answer: {"libraryParts": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Model El
```

## line_arrowheads.json

```
AC29 FRA FAIL 41/44 build local tapir 2.0.1
  x Arrowheads (startArrow/endArrow) of Lines, Polylines, Arcs and Splines: set by CreateLineElements, CreatePolylines, CreateArcs, CreateSplines and SetDetailsOfElements, read back by GetDetailsOfElements; a Circle refuses them / change the arrowheads of the line, polyline, arc and spline; a circle refuses one / spline changed: false (want == true)
  x Arrowheads (startArrow/endArrow) of Lines, Polylines, Arcs and Splines: set by CreateLineElements, CreatePolylines, CreateArcs, CreateSplines and SetDetailsOfElements, read back by GetDetailsOfElements; a Circle refuses them / change the arrowheads of the line, polyline, arc and spline; a circle refuses one / a circle has no ends: true (want == false)
  x Arrowheads (startArrow/endArrow) of Lines, Polylines, Arcs and Splines: set by CreateLineElements, CreatePolylines, CreateArcs, CreateSplines and SetDetailsOfElements, read back by GetDetailsOfElements; a Circle refuses them / read the changed arrowheads back / spline: end arrowhead hidden: true (want == false)
```

## measure_texts_change_text_content.json

```
AC29 FRA FAIL 40/45 build local tapir 2.0.1
  x MeasureTexts measures lines by font, height and style; ChangeTextContent replaces, inserts and deletes and keeps the run styles / the changed content, with the run styles kept / still two runs: [{"text": "Say", "penIndex": 66, "fontIndex": 374, "fontName": "Arial Occidental", "bold": false, "italic": false, "unde (want has 2 items)
  x MeasureTexts measures lines by font, height and style; ChangeTextContent replaces, inserts and deletes and keeps the run styles / the changed content, with the run styles kept / insertion joins the regular run: "Say" (want == "Say ")
  x MeasureTexts measures lines by font, height and style; ChangeTextContent replaces, inserts and deletes and keeps the run styles / the changed content, with the run styles kept / replacement takes the bold run's place: "" (want == "Tapir")
  x MeasureTexts measures lines by font, height and style; ChangeTextContent replaces, inserts and deletes and keeps the run styles / the changed content, with the run styles kept / replacement is bold, like the character at from: false (want == true)
  x MeasureTexts measures lines by font, height and style; ChangeTextContent replaces, inserts and deletes and keeps the run styles / the changed content, with the run styles kept / still two lines, the refused line end not inserted: 1 (want == 2)
```

## mep_elements_and_ports.json

```
AC29 FRA FAIL 27/28 build local tapir 2.0.1
  x CreateMEPElements places terminals that GetMEPElements, GetMEPElementDetails and GetMEPPorts read back; ModifyMEPElements moves one, ModifyMEPPorts changes a flow direction, CheckMEPPortConnectability refuses ports of two domains / connectability / a ventilation port does not connect to a piping port: null (want == false)
```

## mep_preference_tables_segment_rows.json

```
AC29 FRA FAIL 21/23 build local tapir 2.0.1
  x MEP preference tables: a new pipe segment table gets its row set, read, changed by index, emptied and deleted, and bad rows are refused / delete the row / executionResults[0].success: false (want == true)
  x MEP preference tables: a new pipe segment table gets its row set, read, changed by index, emptied and deleted, and bad rows are refused / read the emptied row / no longer valid: true (want != true)
```

## mep_routing_parameters_elbow.json

```
AC29 FRA FAIL 1/6 build local tapir 2.0.1
  x SetMEPRoutingParameters changes the elbow radius factor of a route and of a node, read back by GetMEPRoutingParameters, and refuses node parameters on a route / route elbow radius factor / executionResults[0].success: false (want == true)
  x SetMEPRoutingParameters changes the elbow radius factor of a route and of a node, read back by GetMEPRoutingParameters, and refuses node parameters on a route / node elbow radius factor / executionResults[0].success: false (want == true)
  x SetMEPRoutingParameters changes the elbow radius factor of a route and of a node, read back by GetMEPRoutingParameters, and refuses node parameters on a route / read both / route default: null (want ~= 2.0 +/- 0.001)
  x SetMEPRoutingParameters changes the elbow radius factor of a route and of a node, read back by GetMEPRoutingParameters, and refuses node parameters on a route / read both / node: null (want ~= 1.5 +/- 0.001)
  x SetMEPRoutingParameters changes the elbow radius factor of a route and of a node, read back by GetMEPRoutingParameters, and refuses node parameters on a route / route unchanged / nothing was changed: null (want ~= 2.0 +/- 0.001)
```

## mep_system_groups_and_physical_systems.json

```
AC29 FRA FAIL 48/55 build local tapir 2.0.1
  x MEP system groups and physical systems: CreateMEPSystemGroups, CreateMEPPhysicalSystems, ModifyMEPPhysicalSystems, ModifyMEPSystemGroups and DeleteMEPPhysicalSystems change what GetMEPSystemGroups, GetMEPPhysicalSystemsOfElements and GetMEPDistributionSystems read, and refuse ids that are not theirs / the pipe is in the rooted physical system / physicalSystemsOfElements[0].physicalSystemIds: [] (want has 1 items)
  x MEP system groups and physical systems: CreateMEPSystemGroups, CreateMEPPhysicalSystems, ModifyMEPPhysicalSystems, ModifyMEPSystemGroups and DeleteMEPPhysicalSystems change what GetMEPSystemGroups, GetMEPPhysicalSystemsOfElements and GetMEPDistributionSystems read, and refuse ids that are not theirs / the distribution system of the pipe / the rooted physical system: [] (want has 1 items)
  x MEP system groups and physical systems: CreateMEPSystemGroups, CreateMEPPhysicalSystems, ModifyMEPPhysicalSystems, ModifyMEPSystemGroups and DeleteMEPPhysicalSystems change what GetMEPSystemGroups, GetMEPPhysicalSystemsOfElements and GetMEPDistributionSystems read, and refuse ids that are not theirs / the distribution system of the pipe / tree when asked for: null (want exists)
  x MEP system groups and physical systems: CreateMEPSystemGroups, CreateMEPPhysicalSystems, ModifyMEPPhysicalSystems, ModifyMEPSystemGroups and DeleteMEPPhysicalSystems change what GetMEPSystemGroups, GetMEPPhysicalSystemsOfElements and GetMEPDistributionSystems read, and refuse ids that are not theirs / the pipe is still in it / physicalSystemsOfElements[0].physicalSystemIds: [] (want has 1 items)
  x MEP system groups and physical systems: CreateMEPSystemGroups, CreateMEPPhysicalSystems, ModifyMEPPhysicalSystems, ModifyMEPSystemGroups and DeleteMEPPhysicalSystems change what GetMEPSystemGroups, GetMEPPhysicalSystemsOfElements and GetMEPDistributionSystems read, and refuse ids that are not theirs / the root is the pipe / routingElements[0].domain: null (want == "Piping")
  ... 2 more failures
```

## meshes_floor_plan_and_section.json

```
AC29 FRA FAIL 33/36 build local tapir 2.0.1
  x CreateMeshes, ModifyMeshes and GetDetailsOfElements write and read the floor plan and section settings of a mesh: story visibility, cut fill pens, section contour pen and cover fill (#2630) / read the modified mesh back / detailsOfElements[0].details.floorFill.localOrigin.x: 0 (want ~= 1061.0 +/- 0.001)
  x CreateMeshes, ModifyMeshes and GetDetailsOfElements write and read the floor plan and section settings of a mesh: story visibility, cut fill pens, section contour pen and cover fill (#2630) / read the modified mesh back / detailsOfElements[0].details.floorFill.localOrigin.y: 0 (want ~= 761.0 +/- 0.001)
  x CreateMeshes, ModifyMeshes and GetDetailsOfElements write and read the floor plan and section settings of a mesh: story visibility, cut fill pens, section contour pen and cover fill (#2630) / read the modified mesh back / detailsOfElements[0].details.floorFill.angle: 0 (want ~= 0.5 +/- 0.001)
```

## modify_beams_columns_profile_size.json

```
AC29 FRA FAIL 16/24 build local tapir 2.0.1
  x ModifyColumns and ModifyBeams fail an item whose width/height a custom profile ignores, and still apply its other fields (#2554) / width and depth on the profiled column, with a rotation / names the profile: "depth not applied: the cross section is the profile (unnamed), which sets the size (it stayed 0.45 x 0.550002). Send bu (want contains "Tap
  x ModifyColumns and ModifyBeams fail an item whose width/height a custom profile ignores, and still apply its other fields (#2554) / the size stayed, the rotation applied / width is still the profile's: 0.15000007800000004 (want ~= 0 +/- 0.001)
  x ModifyColumns and ModifyBeams fail an item whose width/height a custom profile ignores, and still apply its other fields (#2554) / the size stayed, the rotation applied / depth is still the profile's: 0.25000172700000006 (want ~= 0 +/- 0.001)
  x ModifyColumns and ModifyBeams fail an item whose width/height a custom profile ignores, and still apply its other fields (#2554) / width and height on the profiled beam, with offset and profile angle / not a silent success: true (want == false)
  x ModifyColumns and ModifyBeams fail an item whose width/height a custom profile ignores, and still apply its other fields (#2554) / width and height on the profiled beam, with offset and profile angle / says the size was not applied: null (want contains "not applied")
  ... 3 more failures
```

## modify_beams_display.json

```
AC29 FRA FAIL 36/38 build local tapir 2.0.1
  x ModifyBeams writes the floor plan display settings GetDetailsOfElements reads for a beam (story visibility, display option, projection modes, shown lines, pens and line types) and refuses an unknown line type without changing the beam / home story only / home story only written: false (want == true)
  x ModifyBeams writes the floor plan display settings GetDetailsOfElements reads for a beam (story visibility, display option, projection modes, shown lines, pens and line types) and refuses an unknown line type without changing the beam / read the story visibility / detailsOfElements[0].details.visibility.showRelAbove: 1 (want == 0)
```

## modify_cameras.json

```
AC29 FRA FAIL 8/28 build local tapir 2.0.1
  x ModifyCameras changes a camera's positions, view cone, two-point perspective, sun and pen and keeps its GUID and path (#2657) / modify camera 1, and refuse a missing camera, a Camera Set and an empty change / camera 1 changed: false (want == true)
  x ModifyCameras changes a camera's positions, view cone, two-point perspective, sun and pen and keeps its GUID and path (#2657) / GetCameras shows the change, the same GUIDs and camera 2 unchanged / camera 1 keeps its GUID: null (want contains "137B19CB-AC33-41B6-B26E-95F6369E8F7B")
  x ModifyCameras changes a camera's positions, view cone, two-point perspective, sun and pen and keeps its GUID and path (#2657) / GetCameras shows the change, the same GUIDs and camera 2 unchanged / cameraSets[*].cameras[*].cameraElementId.guid: null (want contains "2361D0D5-E77C-4F04-AEB4-9901AA32A057")
  x ModifyCameras changes a camera's positions, view cone, two-point perspective, sun and pen and keeps its GUID and path (#2657) / GetCameras shows the change, the same GUIDs and camera 2 unchanged / camera 1 new x: [801.25, 821.5] (want contains 805.5)
  x ModifyCameras changes a camera's positions, view cone, two-point perspective, sun and pen and keeps its GUID and path (#2657) / GetCameras shows the change, the same GUIDs and camera 2 unchanged / camera 1 new y: [802.5, 803.75] (want contains 798.25)
  ... 15 more failures
```

## modify_columns_display.json

```
AC29 FRA FAIL 34/36 build local tapir 2.0.1
  x GetDetailsOfElements reads, and ModifyColumns writes, the floor plan display settings of a column (#2529) / home story only / home story only written: false (want == true)
  x GetDetailsOfElements reads, and ModifyColumns writes, the floor plan display settings of a column (#2529) / read the story visibility back / detailsOfElements[0].details.visibility.showRelAbove: 1 (want == 0)
```

## modify_curtain_walls.json

```
AC29 FRA FAIL 35/37 build local tapir 2.0.1
  x ModifyCurtainWalls writes the floor plan display settings GetDetailsOfElements reads, and keeps the geometry (#2529) / home story only, cut only, entire element, projection modes / display change accepted and read back: false (want == true)
  x ModifyCurtainWalls writes the floor plan display settings GetDetailsOfElements reads, and keeps the geometry (#2529) / read the display settings back / no story above: 1 (want == 0)
```

## modify_objects_story_visibility.json

```
AC29 FRA FAIL 4/5 build local tapir 2.0.1
  x ModifyObjects and ModifyLamps write every field of the story visibility, not only showOnHome (#2821) / create lamp shown on its home story only / save lamp: elements[0].elementId.guid not in answer: {"elements": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Tapir
```

## modify_openings_refused_from_ac29.json

```
AC29 FRA FAIL 9/13 build local tapir 2.0.1
  x ModifyOpenings refuses every item from Archicad 29, names SetOpeningDetails and leaves the opening unchanged / opening before / width as created: null (want ~= 1.0 +/- 0.001)
  x ModifyOpenings refuses every item from Archicad 29, names SetOpeningDetails and leaves the opening unchanged / opening before / height as created: null (want ~= 1.2 +/- 0.001)
  x ModifyOpenings refuses every item from Archicad 29, names SetOpeningDetails and leaves the opening unchanged / opening after / width unchanged: null (want ~= 1.0 +/- 0.001)
  x ModifyOpenings refuses every item from Archicad 29, names SetOpeningDetails and leaves the opening unchanged / opening after / height unchanged: null (want ~= 1.2 +/- 0.001)
```

## modify_railings_rails.json

```
AC29 FRA FAIL 5/8 build local tapir 2.0.1
  x ModifyRailings hides the top rail and changes a rail and a handrail of a segment, refuses rails the segment does not have (#2572) / components of the railing before the change / the segment has a handrail: null (want exists)
  x ModifyRailings hides the top rail and changes a rail and a handrail of a segment, refuses rails the segment does not have (#2572) / ModifyRailings: move the first handrail / handrail change accepted and read back: false (want == true)
  x ModifyRailings hides the top rail and changes a rail and a handrail of a segment, refuses rails the segment does not have (#2572) / components of the railing after the change / save toprail: subelements[0].railingToprails[0].elementId.guid not in answer: {"subelements": [{"railingNodes": [{"elementId": {"guid": "4C0E1F0B-357C-42B
```

## modify_roofs_surfaces.json

```
AC29 FRA FAIL 31/33 build local tapir 2.0.1
  x ModifyRoofs sets and clears the top, side and bottom surfaces and the custom surface of one edge, and keeps the rest (#2433) / read the surfaces / side surface: null (want == "B300A916-1E99-49E0-A224-FBFD65A3F7FB")
  x ModifyRoofs sets and clears the top, side and bottom surfaces and the custom surface of one edge, and keeps the rest (#2433) / read the cleared surfaces / side surface kept: null (want == "B300A916-1E99-49E0-A224-FBFD65A3F7FB")
```

## modify_shells.json

```
AC29 FRA FAIL 25/27 build local tapir 2.0.1
  x ModifyShells sets the thickness and the flip of a Basic shell, keeps its reference surface and refuses a thickness on a Composite shell (#2424) / read the flipped shell / isFlipped written: false (want == true)
  x ModifyShells sets the thickness and the flip of a Basic shell, keeps its reference surface and refuses a thickness on a Composite shell (#2424) / the flipped shell's box / the body moved 0.24 m to the other side of the reference surface: 0.0 (want ~= 0.0576 +/- 0.001)
```

## modify_shells_contour_holes.json

```
AC29 FRA FAIL 29/34 build local tapir 2.0.1
  x GetDetailsOfElements reads a shell's contour and holes, ModifyShells replaces them and keeps the shell (#2431) / same shell, new contour and depth, the rest kept / second hole's new depth: 10 (want ~= 5.0 +/- 0.001)
  x GetDetailsOfElements reads a shell's contour and holes, ModifyShells replaces them and keeps the shell (#2431) / same shell, new contour and depth, the rest kept / second hole's new plane: 0 (want ~= 1.0 +/- 0.001)
  x GetDetailsOfElements reads a shell's contour and holes, ModifyShells replaces them and keeps the shell (#2431) / the holes survived the contour change / detailsOfElements[0].details.holes[1].depth: 10 (want ~= 5.0 +/- 0.001)
  x GetDetailsOfElements reads a shell's contour and holes, ModifyShells replaces them and keeps the shell (#2431) / no contour and no holes left, still one shell / contour removed: {"coordinates": [{"x": -2.5, "y": 0.5}, {"x": 2.5, "y": 0.5}, {"x": 2.5, "y": 7.5}, {"x": -2.5, "y": 7.5}], "plane": {"o (want missing)
  x GetDetailsOfElements reads a shell's contour and holes, ModifyShells replaces them and keeps the shell (#2431) / no contour and no holes left, still one shell / holes removed: [{"coordinates": [{"x": -1, "y": 2}, {"x": 1, "y": 2}, {"x": 1, "y": 3}, {"x": -1, "y": 3}], "plane": {"origin": {"x": 0 (want has 0 items)
```

## modify_shells_edge_surfaces.json

```
AC29 FRA FAIL 25/34 build local tapir 2.0.1
  x GetDetailsOfElements reads and ModifyShells sets and clears the custom surface of individual shell edges, and keeps the other edges and faces (#2433) / read the edges / begin profile edges surface: "B300A916-1E99-49E0-A224-FBFD65A3F7FB" (want == "B1D0836F-CD73-4474-8119-84BAA7497202")
  x GetDetailsOfElements reads and ModifyShells sets and clears the custom surface of individual shell edges, and keeps the other edges and faces (#2433) / read the edges / end profile edges not overridden (refused item changed nothing): true (want == false)
  x GetDetailsOfElements reads and ModifyShells sets and clears the custom surface of individual shell edges, and keeps the other edges and faces (#2433) / read the edges / first side edge surface: "B300A916-1E99-49E0-A224-FBFD65A3F7FB" (want == "B1D0836F-CD73-4474-8119-84BAA7497202")
  x GetDetailsOfElements reads and ModifyShells sets and clears the custom surface of individual shell edges, and keeps the other edges and faces (#2433) / read the edges / last side edge not overridden (refused item changed nothing): true (want == false)
  x GetDetailsOfElements reads and ModifyShells sets and clears the custom surface of individual shell edges, and keeps the other edges and faces (#2433) / the changed edges, and the other edges and faces kept / begin profile edges cleared: true (want == false)
  ... 4 more failures
```

## modify_shells_flip.json

```
AC29 FRA FAIL 14/23 build local tapir 2.0.1
  x GetDetailsOfElements reads and ModifyShells sets the Flip of an existing shell, which moves its body to the other side (#2432) / the flipped shell, read by its old GUID, keeps its thickness, class and structure / now flipped: false (want == true)
  x GetDetailsOfElements reads and ModifyShells sets the Flip of an existing shell, which moves its body to the other side (#2432) / the flipped shell's body is where the shell flipped at creation has it / xMin as the flipped shell's, 20 m away: -20.14154052699996 (want ~= -20 +/- 0.001)
  x GetDetailsOfElements reads and ModifyShells sets the Flip of an existing shell, which moves its body to the other side (#2432) / the flipped shell's body is where the shell flipped at creation has it / xMax as the flipped shell's, 20 m away: -19.85852050799997 (want ~= -20 +/- 0.001)
  x GetDetailsOfElements reads and ModifyShells sets the Flip of an existing shell, which moves its body to the other side (#2432) / the flipped shell's body is where the shell flipped at creation has it / zMin as the flipped shell's: 0.141481251 (want ~= 0 +/- 0.001)
  x GetDetailsOfElements reads and ModifyShells sets the Flip of an existing shell, which moves its body to the other side (#2432) / the flipped shell's body is where the shell flipped at creation has it / zMax as the flipped shell's: 0.200457812 (want ~= 0 +/- 0.001)
  ... 4 more failures
```

## modify_shells_surfaces.json

```
AC29 FRA FAIL 26/27 build local tapir 2.0.1
  x GetDetailsOfElements reads and ModifyShells sets and clears the top, side and bottom surfaces of a shell, and keeps the rest (#2433) / read the surfaces / thickness kept: 0.3 (want ~= 0.2 +/- 0.001)
```

## modify_skylights.json

```
AC29 FRA FAIL 25/28 build local tapir 2.0.1
  x ModifySkylights changes a skylight's settings, CreateSkylights takes the same keys, GetDetailsOfElements reads them back / read the created skylight / created display option: "CutOnly" (want == "CutAll")
  x ModifySkylights changes a skylight's settings, CreateSkylights takes the same keys, GetDetailsOfElements reads them back / read back the changes / azimuth changed: 0 (want ~= 0.3 +/- 1e-06)
  x ModifySkylights changes a skylight's settings, CreateSkylights takes the same keys, GetDetailsOfElements reads them back / read back the changes / display option changed: "CutOnly" (want == "OutLinesOnly")
```

## modify_slabs_edge_trims.json

```
AC29 FRA FAIL 26/27 build local tapir 2.0.1
  x GetDetailsOfElements reports and ModifySlabs writes the Edge Angle of every edge and of each edge, and the custom surface of one edge of a slab (#2562) / read each edge / slab side surface kept: null (want == "B300A916-1E99-49E0-A224-FBFD65A3F7FB")
```

## modify_stairs.json

```
AC29 FRA FAIL 15/16 build local tapir 2.0.1
  x ModifyStairs writes the floor plan and the reflected ceiling plan display of a stair independently: shown stories, walking line and structure (#2530) / a bad story visibility is refused by the schema / refused: null (want exists)
```

## modify_stairs_going.json

```
AC29 FRA FAIL 5/8 build local tapir 2.0.1
  x ModifyStairs lays a stair out with a new going (treadDepth) (#2525) / the going as created / going 0.28 as created: "0,28" (want ~= 0.28 +/- 0.005)
  x ModifyStairs lays a stair out with a new going (treadDepth) (#2525) / change the going to 0.26 / accepted: false (want == true)
  x ModifyStairs lays a stair out with a new going (treadDepth) (#2525) / the going after ModifyStairs / going changed to 0.26: "0,28" (want ~= 0.26 +/- 0.005)
```

## navigator_items_move_rename_reorder_delete.json

```
AC29 FRA FAIL 41/43 build local tapir 2.0.1
  x Navigator items: GetNavigatorItemTree, GetNavigatorParentItems, MoveNavigatorItem, ReorderNavigatorItems, RenameNavigatorItem and DeleteNavigatorItems on View Map folders, and refuse bad input / [delete C, A, B, the folder, and an item that does not exist] / folder, empty now: false (want == true)
  x Navigator items: GetNavigatorItemTree, GetNavigatorParentItems, MoveNavigatorItem, ReorderNavigatorItems, RenameNavigatorItem and DeleteNavigatorItems on View Map folders, and refuse bad input / the folder is gone / navigatorItemTree.children[1].navigatorItem.name: "Tapir check folder" (want != "Tapir check folder")
```

## objects_and_lamps_create_modify.json

```
AC29 FRA FAIL 4/5 build local tapir 2.0.1
  x CreateObjects, ModifyObjects, CreateLamps and ModifyLamps write what they are sent, and refuse bad input without changing anything / create lamp / save lamp: elements[0].elementId.guid not in answer: {"elements": [{"error": {"code": -2130313113, "message": "Not found library part with name 'Tapir
```

## openings_create_get_set_details.json

```
AC29 FRA FAIL 26/28 build local tapir 2.0.1
  x CreateOpenings cuts the wall it is given, GetOpeningDetails reads it and SetOpeningDetails changes its shape, size, anchor and position, and refuses a bad surface without changing anything / move 0.5 along X / executionResults[0].success: false (want == true)
  x CreateOpenings cuts the wall it is given, GetOpeningDetails reads it and SetOpeningDetails changes its shape, size, anchor and position, and refuses a bad surface without changing anything / read the move / moved 0.5 along X: 0.0 (want ~= 0.5 +/- 0.001)
```

## project_info_groups.json

```
AC29 FRA FAIL 0/0 build local tapir 2.0.1
```

## property_groups_and_definitions.json

```
AC29 FRA FAIL 3/4 build local tapir 2.0.1
  x Property groups and definitions: create, read back with GetAllProperties, update and delete / [string in A by id, single enum in B by name, expression in A, group that does not exist] / save propEnum: propertyIds[1].propertyId.guid not in answer: {"propertyIds": [{"propertyId": {"guid": "47D35311-D49A-4B25-9F9F-F4DFB3D783FC"}}, {"error": {
```

## property_values_of_attributes.json

```
AC29 FRA FAIL 43/44 build local tapir 2.0.1
  x Property definitions and values of attributes: read, write, built-in values, add and remove (#1921) / built-in Description property / save description: properties[0].propertyId.guid not in answer: {"properties": [{"error": {"code": 4005, "message": "Property definition not found (nonLocalize
```

## railings_stairs_modify.json

```
AC29 FRA FAIL 60/62 build local tapir 2.0.1
  x ModifyRailings and ModifyStairs: every change read back, bad inputs refused / stair after the finish change / finishes hidden: true (want == false)
  x ModifyRailings and ModifyStairs: every change read back, bad inputs refused / the refused items changed nothing / stair finishes still hidden: true (want == false)
```

## recreate_stairs.json

```
AC29 FRA FAIL 19/21 build local tapir 2.0.1
  x RecreateStairs moves the end of a U stair's second flight: a new stair with the old Element ID, story and settings, the old one deleted; a refused baseline changes nothing (#2532) / the refused baseline left the stair as it was / with its old baseline: 711.44 (want ~= 710.0 +/- 0.001)
  x RecreateStairs moves the end of a U stair's second flight: a new stair with the old Element ID, story and settings, the old one deleted; a refused baseline changes nothing (#2532) / read the new and the old stair / the second flight ends at the new point: 711.44 (want ~= 710.5 +/- 0.01)
```

## rename_navigator_item_autotext.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x RenameNavigatorItem with autotext tokens in the new name reports success, and GetNavigatorItemTree reads the custom name back (#2499) / a story of the Project Map / first item of the first Project Map group is a story: "UndefinedItem" (want == "StoryItem")
```

## reorder_navigator_items_without_sibling_folder.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x ReorderNavigatorItems reorders a View Map folder that holds only views and a clone folder, with no sibling folder to bounce through (#2701) / the stories group and a story of the Project Map / first item of the first Project Map group is a story: "UndefinedItem" (want == "StoryItem")
```

## roof_shell_cut_body_type.json

```
AC29 FRA FAIL 21/22 build local tapir 2.0.1
  x ModifyRoofs and ModifyShells set the trimming body (cutBodyType), GetDetailsOfElements reads it back and a trim stays / the shell has Upward Extrusion / thickness kept: 0.3 (want ~= 0.2 +/- 0.001)
```

## search_and_criteria.json

```
AC29 FRA FAIL 11/13 build local tapir 2.0.1
  x Search properties, search favorites and get elements by criteria / search properties by query / property guid found: null (want exists)
  x Search properties, search favorites and get elements by criteria / search properties by query / property name found: null (want exists)
```

## search_properties.json

```
AC29 FRA FAIL 1/3 build local tapir 2.0.1
  x SearchProperties command / search properties by query / property guid found: null (want exists)
  x SearchProperties command / search properties by query / property name found: null (want exists)
```

## sections_and_interior_elevations.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x CreateSections, ModifySections and CreateInteriorElevations: geometry, name and ID read back, bad input refused / - / scratch project: the project already contains 2 CutPlane element(s)
```

## set_3d_filter_and_cut_keeps_mep_routes.json

```
AC29 FRA FAIL 6/8 build local tapir 2.0.1
  x Set3DFilterAndCutSettings with the settings already in force, or with one element type, keeps the MEP routes visible in 3D (#2614) / both routes still visible / pipe and duct still shown (#2614): [] (want has 2 items)
  x Set3DFilterAndCutSettings with the settings already in force, or with one element type, keeps the MEP routes visible in 3D (#2614) / both routes visible after an element type change / pipe and duct still shown: [] (want has 2 items)
```

## set_details_of_elements_opening_id_layer.json

```
AC29 FRA FAIL 7/9 build local tapir 2.0.1
  x SetDetailsOfElements sets the id and the layer of an Opening placed with PlaceOpenings, and GetDetailsOfElements reads them back and points to GetOpeningDetails for the rest (#2629) / set id and layer of the opening / id and layer set: false (want == true)
  x SetDetailsOfElements sets the id and the layer of an Opening placed with PlaceOpenings, and GetDetailsOfElements reads them back and points to GetOpeningDetails for the rest (#2629) / read the opening back / layer applied: -9.0 (want ~= 0 +/- 0.001)
```

## set_layout_settings_master_rename.json

```
AC29 FRA FAIL 9/16 build local tapir 2.0.1
  x SetLayoutSettings renames a master layout by its database id and by its navigator item (#2524) / [rename the master by its database id] / master renamed: false (want == true)
  x SetLayoutSettings renames a master layout by its database id and by its navigator item (#2524) / the layout shows the new master name / new name read back: "Tapir check rename master" (want == "Tapir check master renamed")
  x SetLayoutSettings renames a master layout by its database id and by its navigator item (#2524) / the layout shows the new master name / layout name kept: "03.1 Tapir check rename layout" (want == "Tapir check rename layout")
  x SetLayoutSettings renames a master layout by its database id and by its navigator item (#2524) / [rename the master by its navigator item] / master renamed: false (want == true)
  x SetLayoutSettings renames a master layout by its database id and by its navigator item (#2524) / the layout shows the second master name, the master keeps its size / second name read back: "Tapir check rename master" (want == "Tapir check master renamed twice")
  ... 2 more failures
```

## set_library_part_parameters.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x GetGDLParametersOfLibraryParts and SetLibraryPartParameters find the same embedded library part with and without the .gsm extension (#2527) / embedded library part / part created: null (want == "TapirCheck2527")
```

## set_library_part_parameters_values_2776.json

```
AC29 FRA FAIL 6/10 build local tapir 2.0.1
  x SetLibraryPartParameters changes the default values GetLibraryPartParameterValues reads of an embedded library part, after the change that modifies a part of a local folder library in its file (#2776; the local folder path itself needs a saved project with a library folder and is not run here; from AC29, because Archicad 28 does not report a part of the embedded library editable, which this change does not touch) / [set A, missing part] / the part is set: false (want == true)
  x SetLibraryPartParameters changes the default values GetLibraryPartParameterValues reads of an embedded library part, after the change that modifies a part of a local folder library in its file (#2776; the local folder path itself needs a saved project with a library folder and is not run here; from AC29, because Archicad 28 does not report a part of the embedded library editable, which this change does not touch) / A after the set / A is the new value: 1 (want ~= 1.123 +/- 0.001)
  x SetLibraryPartParameters changes the default values GetLibraryPartParameterValues reads of an embedded library part, after the change that modifies a part of a local folder library in its file (#2776; the local folder path itself needs a saved project with a library folder and is not run here; from AC29, because Archicad 28 does not report a part of the embedded library editable, which this change does not touch) / set A again, merged / the merge is set: false (want == true)
  x SetLibraryPartParameters changes the default values GetLibraryPartParameterValues reads of an embedded library part, after the change that modifies a part of a local folder library in its file (#2776; the local folder path itself needs a saved project with a library folder and is not run here; from AC29, because Archicad 28 does not report a part of the embedded library editable, which this change does not touch) / A after the merge / A is the merged value: 1 (want ~= 1.5 +/- 0.001)
```

## set_view_settings_renovation_filter_name.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x SetViewSettings sets the renovation filter by renovationFilterName and fails an unknown or conflicting name without writing (#2700) / a story of the Project Map / first item of the first Project Map group is a story: "UndefinedItem" (want == "StoryItem")
```

## slabs_auto_story_visibility.json

```
AC29 FRA FAIL 5/7 build local tapir 2.0.1
  x CreateSlabs and ModifySlabs write isAutoOnStoryVisibility of a slab, and a given visibility turns it off (#2561) / a given visibility turns the automatic one off / visibility applied: false (want == true)
  x CreateSlabs and ModifySlabs write isAutoOnStoryVisibility of a slab, and a given visibility turns it off (#2561) / read the custom visibility / contour on all stories above: false (want == true)
```

## slabs_floor_plan_display.json

```
AC29 FRA FAIL 29/35 build local tapir 2.0.1
  x CreateSlabs and ModifySlabs write the floor plan and section display of a slab, GetDetailsOfElements reads it back, and an unknown line type is refused (#2561) / read the new slab / geometry kept: 0.35 (want ~= 0.25 +/- 0.001)
  x CreateSlabs and ModifySlabs write the floor plan and section display of a slab, GetDetailsOfElements reads it back, and an unknown line type is refused (#2561) / change the display of the slab / every display setting applied: false (want == true)
  x CreateSlabs and ModifySlabs write the floor plan and section display of a slab, GetDetailsOfElements reads it back, and an unknown line type is refused (#2561) / read the changed slab / thickness kept: 0.35 (want ~= 0.25 +/- 0.001)
  x CreateSlabs and ModifySlabs write the floor plan and section display of a slab, GetDetailsOfElements reads it back, and an unknown line type is refused (#2561) / read the changed slab / contour no longer above: true (want == false)
  x CreateSlabs and ModifySlabs write the floor plan and section display of a slab, GetDetailsOfElements reads it back, and an unknown line type is refused (#2561) / read the changed slab / contour on all stories below: false (want == true)
  ... 1 more failures
```

## stairs_shared_settings.json

```
AC29 FRA FAIL 15/16 build local tapir 2.0.1
  x CreateStairs and ModifyStairs accept the same settings: treads, structures, walking line and numbering on creation, the new settings on modification, bad values refused / ModifyStairs: a bad walking line position is refused by the shared schema / ModifyStairs: rejected: {"code": 4002, "message": "Invalid command parameters (The JSON is invalid according to the JSON schema. Validation failed on sche
```

## structure_display.json

```
AC29 FRA FAIL 14/15 build local tapir 2.0.1
  x SetStructureDisplay changes the Partial Structure Display of the floor plan and the 3D window, GetStructureDisplay reads it back / bad input: unknown value / refused by the input schema (PartialStructureDisplay enum): null (want exists)
```

## tool_default_properties_in_section_window.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x GetPropertiesOfToolDefaults and GetPropertyValuesOfElementDefaults answer for the Label tool from a Section window instead of ending Archicad / - / scratch project: the project already contains 2 CutPlane element(s)
```

## view_map_folders_views_and_settings.json

```
AC29 FRA FAIL 0/1 build local tapir 2.0.1
  x View Map: CreateViewMapFolder, CloneProjectMapItemToViewMap and CreateViewsInViewMap put their items in the given folder, SetViewSettings changes what GetViewSettings reads / a story of the Project Map / first item of the first Project Map group is a story: "UndefinedItem" (want == "StoryItem")
```

## zone_cover_fill_orientation.json

```
AC29 FRA FAIL 19/23 build local tapir 2.0.1
  x Zone cover fill: use the surface's fill and the fill orientation in CreateZones, ModifyZones, SetDetailsOfElements and GetDetailsOfElements (#2631) / read the modified zone / fill angle changed: 0.5 (want ~= 1.0 +/- 0.001)
  x Zone cover fill: use the surface's fill and the fill orientation in CreateZones, ModifyZones, SetDetailsOfElements and GetDetailsOfElements (#2631) / read the moved fill origin / fill origin moved: 941 (want ~= 942.5 +/- 0.001)
  x Zone cover fill: use the surface's fill and the fill orientation in CreateZones, ModifyZones, SetDetailsOfElements and GetDetailsOfElements (#2631) / read the moved fill origin / detailsOfElements[0].details.coverFill.locOrigo.y: 721 (want ~= 722.0 +/- 0.001)
  x Zone cover fill: use the surface's fill and the fill orientation in CreateZones, ModifyZones, SetDetailsOfElements and GetDetailsOfElements (#2631) / read the moved fill origin / fill angle kept: 0.5 (want ~= 1.0 +/- 0.001)
```
