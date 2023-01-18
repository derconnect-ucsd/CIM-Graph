from typing import List
from dataclasses import dataclass, field

import cim.data_profile as cim


def get_all_attributes(feeder_id: str, mrid_list: List[str]):
    query_message = """
        PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX cim: <http://iec.ch/TC57/CIM100#>
        SELECT ?mRID ?name ?coreRadius ?coreStrandCount ?gmr ?insulated ?insulationMaterial 
         ?insulationThickness ?material ?rAC25 ?rAC50 ?rAC75 ?rDC20 ?radius ?ratedCurrent ?strandCount
         ?sizeDescription 
         (group_concat(distinct ?ACLineSegmentPhase; separator=';') as ?ACLineSegmentPhases)
        WHERE {          
          ?eq r:type cim:OverheadWireInfo.
          VALUES ?fdrid {"%s"}
          VALUES ?mRID {"""%feeder_id
    # add all equipment mRID
    for mrid in mrid_list:
        query_message += ' "%s" \n'%mrid
    # add all attributes
    query_message += """               } 
        #trace back up to EquipmentContainer via ACLineSegment
        ?fdr cim:IdentifiedObject.mRID ?fdrid.
        ?line cim:Equipment.EquipmentContainer ?fdr.
        ?linephase cim:ACLineSegmentPhase.ACLineSegment ?line.
        ?linephase cim:ACLineSegmentPhase.WireInfo ?eq.
        ?linephase cim:IdentifiedObject.mRID ?ACLineSegmentPhase.

        ?eq cim:IdentifiedObject.mRID ?mRID.
        ?eq cim:IdentifiedObject.name ?name.
        
        #collect inherited WireInfo attributes
        OPTIONAL {?eq cim:WireInfo.coreRadius ?coreRadius.}
        OPTIONAL {?eq cim:WireInfo.coreStrandCount ?coreStrandCount.}        
        OPTIONAL {?eq cim:WireInfo.gmr ?gmr.}
        OPTIONAL {?eq cim:WireInfo.insulated ?insulated.} 
        OPTIONAL {?eq cim:WireInfo.insulationMaterial ?ins.
                  bind(strafter(str(?ins),"WireInsulationKind.") as ?insulationMaterial).}
        OPTIONAL {?eq cim:WireInfo.insulationThickness ?insulationThickness.}
        OPTIONAL {?eq cim:WireInfo.material ?material.}
        OPTIONAL {?eq cim:WireInfo.rAC25 ?rAC25.}
        OPTIONAL {?eq cim:WireInfo.rAC50 ?rAC50.}
        OPTIONAL {?eq cim:WireInfo.rAC75 ?rAC75.}
        OPTIONAL {?eq cim:WireInfo.rDC20 ?rDC20.}
        OPTIONAL {?eq cim:WireInfo.radius ?radius.}
        OPTIONAL {?eq cim:WireInfo.ratedCurrent ?ratedCurrent.}
        OPTIONAL {?eq cim:WireInfo.strandCount ?strandCount.}
        OPTIONAL {?eq cim:WireInfo.sizeDescription ?sizeDescription.}


        }
        GROUP BY ?mRID ?name ?coreRadius ?coreStrandCount ?gmr ?insulated ?insulationMaterial 
         ?insulationThickness ?material ?rAC25 ?rAC50 ?rAC75 ?rDC20 ?radius ?ratedCurrent ?strandCount
         ?sizeDescription
         
        ORDER by  ?name
        """
    return query_message