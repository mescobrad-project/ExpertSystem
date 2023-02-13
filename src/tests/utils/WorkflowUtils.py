from sqlalchemy.orm import Session
from uuid import UUID
from src.controllers.WorkflowController import WorkflowController
from src.models._all import WorkflowModel
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate
from src.utils.workflow import parse_xml
from ._base import (
    random_lower_string,
    random_unique_string,
    random_dict_obj,
    random_bool,
)
from .WorkflowCategoryUtils import seed_category


def create_random_workflow(used_xml_times) -> tuple[str, dict]:
    name = random_unique_string()
    description = random_lower_string()
    raw_diagram_data = random_dict_obj()
    if used_xml_times == 0:
        raw_diagram_data[
            "xml_original"
        ] = '<?xml version="1.0" encoding="UTF-8"?>\n<bpmn2:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="sample-diagram" targetNamespace="http://bpmn.io/schema/bpmn" xsi:schemaLocation="http://www.omg.org/spec/BPMN/20100524/MODEL BPMN20.xsd">\n  <bpmn2:process id="Process_1" isExecutable="false">\n    <bpmn2:startEvent id="StartEvent_1">\n      <bpmn2:outgoing>Flow_1lgia7a</bpmn2:outgoing>\n    </bpmn2:startEvent>\n    <bpmn2:sequenceFlow id="Flow_1lgia7a" sourceRef="StartEvent_1" targetRef="Activity_04n854t" />\n    <bpmn2:userTask id="Activity_04n854t" name="Get Dataa">\n      <bpmn2:incoming>Flow_1lgia7a</bpmn2:incoming>\n      <bpmn2:incoming>Flow_13vzrog</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_1bzku7m</bpmn2:outgoing>\n      <bpmn2:property id="Property_0cy4n2t" name="__targetRef_placeholder" />\n      <bpmn2:dataInputAssociation id="DataInputAssociation_1sx6s96">\n        <bpmn2:sourceRef>DataObjectReference_1pdq0fp</bpmn2:sourceRef>\n        <bpmn2:targetRef>Property_0cy4n2t</bpmn2:targetRef>\n      </bpmn2:dataInputAssociation>\n    </bpmn2:userTask>\n    <bpmn2:sequenceFlow id="Flow_1bzku7m" sourceRef="Activity_04n854t" targetRef="Activity_1rtdcjw" />\n    <bpmn2:sendTask id="Activity_1rtdcjw" name="Train dataset with SVN regression">\n      <bpmn2:incoming>Flow_1bzku7m</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_08ndfxw</bpmn2:outgoing>\n    </bpmn2:sendTask>\n    <bpmn2:sequenceFlow id="Flow_08ndfxw" sourceRef="Activity_1rtdcjw" targetRef="Activity_170nkyh" />\n    <bpmn2:receiveTask id="Activity_170nkyh" name="Wait for SVN results">\n      <bpmn2:incoming>Flow_08ndfxw</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_04sv0kp</bpmn2:outgoing>\n      <bpmn2:dataOutputAssociation id="DataOutputAssociation_0e8q8fl">\n        <bpmn2:targetRef>DataObjectReference_1pdq0fp</bpmn2:targetRef>\n      </bpmn2:dataOutputAssociation>\n    </bpmn2:receiveTask>\n    <bpmn2:exclusiveGateway id="Gateway_10nvp31" name="Train another model, or make predictions?">\n      <bpmn2:incoming>Flow_04sv0kp</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_13vzrog</bpmn2:outgoing>\n      <bpmn2:outgoing>Flow_0aez006</bpmn2:outgoing>\n    </bpmn2:exclusiveGateway>\n    <bpmn2:sequenceFlow id="Flow_04sv0kp" sourceRef="Activity_170nkyh" targetRef="Gateway_10nvp31" />\n    <bpmn2:sequenceFlow id="Flow_13vzrog" sourceRef="Gateway_10nvp31" targetRef="Activity_04n854t" />\n    <bpmn2:sequenceFlow id="Flow_0aez006" sourceRef="Gateway_10nvp31" targetRef="Activity_0jk2vbm" />\n    <bpmn2:sendTask id="Activity_0jk2vbm" name="Get predictions with SVN regression">\n      <bpmn2:incoming>Flow_0aez006</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_18h9ys5</bpmn2:outgoing>\n    </bpmn2:sendTask>\n    <bpmn2:sequenceFlow id="Flow_18h9ys5" sourceRef="Activity_0jk2vbm" targetRef="Activity_1mf9ojj" />\n    <bpmn2:receiveTask id="Activity_1mf9ojj" name="Wait for the SVN predictions">\n      <bpmn2:incoming>Flow_18h9ys5</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_150fnaw</bpmn2:outgoing>\n    </bpmn2:receiveTask>\n    <bpmn2:endEvent id="Event_0ii5ket" name="success">\n      <bpmn2:incoming>Flow_150fnaw</bpmn2:incoming>\n    </bpmn2:endEvent>\n    <bpmn2:sequenceFlow id="Flow_150fnaw" sourceRef="Activity_1mf9ojj" targetRef="Event_0ii5ket" />\n    <bpmn2:dataObjectReference id="DataObjectReference_1pdq0fp" name="Data Lake Object Storage" dataObjectRef="DataObject_1lb20ak" />\n    <bpmn2:dataObject id="DataObject_1lb20ak" />\n    <bpmn2:textAnnotation id="TextAnnotation_1vm9mo3">\n      <bpmn2:text>regression/svn/train</bpmn2:text>\n    </bpmn2:textAnnotation>\n    <bpmn2:association id="Association_1ggrhki" sourceRef="Activity_1rtdcjw" targetRef="TextAnnotation_1vm9mo3" />\n    <bpmn2:textAnnotation id="TextAnnotation_1bq4pru">\n      <bpmn2:text>regression/svn/predict</bpmn2:text>\n    </bpmn2:textAnnotation>\n    <bpmn2:association id="Association_1ol8pcm" sourceRef="Activity_0jk2vbm" targetRef="TextAnnotation_1bq4pru" />\n  </bpmn2:process>\n  <bpmndi:BPMNDiagram id="BPMNDiagram_1">\n    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">\n      <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1">\n        <dc:Bounds x="162" y="240" width="36" height="36" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_1rddusr_di" bpmnElement="Activity_04n854t">\n        <dc:Bounds x="250" y="218" width="100" height="80" />\n        <bpmndi:BPMNLabel />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_0i93506_di" bpmnElement="Activity_1rtdcjw">\n        <dc:Bounds x="410" y="218" width="100" height="80" />\n        <bpmndi:BPMNLabel />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_1ik1tjp_di" bpmnElement="Activity_170nkyh">\n        <dc:Bounds x="570" y="218" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Gateway_10nvp31_di" bpmnElement="Gateway_10nvp31" isMarkerVisible="true">\n        <dc:Bounds x="735" y="233" width="50" height="50" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="722" y="290" width="76" height="40" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_1tkr1an_di" bpmnElement="Activity_0jk2vbm">\n        <dc:Bounds x="850" y="218" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_11lztok_di" bpmnElement="Activity_1mf9ojj">\n        <dc:Bounds x="1020" y="218" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Event_0ii5ket_di" bpmnElement="Event_0ii5ket">\n        <dc:Bounds x="1192" y="240" width="36" height="36" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="1190" y="283" width="41" height="14" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="DataObjectReference_1pdq0fp_di" bpmnElement="DataObjectReference_1pdq0fp">\n        <dc:Bounds x="442" y="365" width="36" height="50" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="417" y="422" width="86" height="27" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="TextAnnotation_1vm9mo3_di" bpmnElement="TextAnnotation_1vm9mo3">\n        <dc:Bounds x="520" y="110" width="100" height="41" />\n        <bpmndi:BPMNLabel />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="TextAnnotation_1bq4pru_di" bpmnElement="TextAnnotation_1bq4pru">\n        <dc:Bounds x="950" y="130" width="100" height="41" />\n        <bpmndi:BPMNLabel />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNEdge id="Flow_1lgia7a_di" bpmnElement="Flow_1lgia7a">\n        <di:waypoint x="198" y="258" />\n        <di:waypoint x="250" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="DataInputAssociation_1sx6s96_di" bpmnElement="DataInputAssociation_1sx6s96">\n        <di:waypoint x="442" y="390" />\n        <di:waypoint x="300" y="390" />\n        <di:waypoint x="300" y="298" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_1bzku7m_di" bpmnElement="Flow_1bzku7m">\n        <di:waypoint x="350" y="258" />\n        <di:waypoint x="410" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_08ndfxw_di" bpmnElement="Flow_08ndfxw">\n        <di:waypoint x="510" y="258" />\n        <di:waypoint x="570" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="DataOutputAssociation_0e8q8fl_di" bpmnElement="DataOutputAssociation_0e8q8fl">\n        <di:waypoint x="620" y="298" />\n        <di:waypoint x="620" y="390" />\n        <di:waypoint x="478" y="390" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_04sv0kp_di" bpmnElement="Flow_04sv0kp">\n        <di:waypoint x="670" y="258" />\n        <di:waypoint x="735" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_13vzrog_di" bpmnElement="Flow_13vzrog">\n        <di:waypoint x="760" y="233" />\n        <di:waypoint x="760" y="170" />\n        <di:waypoint x="300" y="170" />\n        <di:waypoint x="300" y="218" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_0aez006_di" bpmnElement="Flow_0aez006">\n        <di:waypoint x="785" y="258" />\n        <di:waypoint x="850" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_18h9ys5_di" bpmnElement="Flow_18h9ys5">\n        <di:waypoint x="950" y="258" />\n        <di:waypoint x="1020" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_150fnaw_di" bpmnElement="Flow_150fnaw">\n        <di:waypoint x="1120" y="258" />\n        <di:waypoint x="1192" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Association_1ggrhki_di" bpmnElement="Association_1ggrhki">\n        <di:waypoint x="493" y="218" />\n        <di:waypoint x="548" y="151" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Association_1ol8pcm_di" bpmnElement="Association_1ol8pcm">\n        <di:waypoint x="935" y="218" />\n        <di:waypoint x="977" y="171" />\n      </bpmndi:BPMNEdge>\n    </bpmndi:BPMNPlane>\n  </bpmndi:BPMNDiagram>\n</bpmn2:definitions>\n'
    else:
        raw_diagram_data[
            "xml_original"
        ] = '<?xml version="1.0" encoding="UTF-8"?>\n<bpmn2:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="sample-diagram" targetNamespace="http://bpmn.io/schema/bpmn" xsi:schemaLocation="http://www.omg.org/spec/BPMN/20100524/MODEL BPMN20.xsd">\n  <bpmn2:process id="Process_1" isExecutable="false">\n    <bpmn2:startEvent id="StartEvent_1">\n      <bpmn2:outgoing>Flow_0j985y1</bpmn2:outgoing>\n    </bpmn2:startEvent>\n    <bpmn2:sequenceFlow id="Flow_0j985y1" sourceRef="StartEvent_1" targetRef="Activity_17z1a6q" />\n    <bpmn2:userTask id="Activity_17z1a6q" name="Get Data">\n      <bpmn2:incoming>Flow_0j985y1</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_0slvwa6</bpmn2:outgoing>\n      <bpmn2:property id="Property_01axr8m" name="__targetRef_placeholder" />\n      <bpmn2:dataInputAssociation id="DataInputAssociation_1h642dx">\n        <bpmn2:sourceRef>DataObjectReference_19g0qyl</bpmn2:sourceRef>\n        <bpmn2:targetRef>Property_01axr8m</bpmn2:targetRef>\n      </bpmn2:dataInputAssociation>\n    </bpmn2:userTask>\n    <bpmn2:sequenceFlow id="Flow_0slvwa6" sourceRef="Activity_17z1a6q" targetRef="Activity_0jngfnp" />\n    <bpmn2:sequenceFlow id="Flow_0m89608" sourceRef="Activity_0jngfnp" targetRef="Activity_1yr2yzs" />\n    <bpmn2:endEvent id="Event_0ue1epw" name="Success">\n      <bpmn2:incoming>Flow_0iofx8s</bpmn2:incoming>\n    </bpmn2:endEvent>\n    <bpmn2:sequenceFlow id="Flow_0iofx8s" sourceRef="Activity_1yr2yzs" targetRef="Event_0ue1epw" />\n    <bpmn2:receiveTask id="Activity_1yr2yzs" name="Wait for results (SNV model)">\n      <bpmn2:incoming>Flow_0m89608</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_0iofx8s</bpmn2:outgoing>\n      <bpmn2:dataOutputAssociation id="DataOutputAssociation_0wylqdr">\n        <bpmn2:targetRef>DataObjectReference_19g0qyl</bpmn2:targetRef>\n      </bpmn2:dataOutputAssociation>\n    </bpmn2:receiveTask>\n    <bpmn2:dataObjectReference id="DataObjectReference_19g0qyl" name="Data Lake Object Storage" dataObjectRef="DataObject_1ywy56n" />\n    <bpmn2:dataObject id="DataObject_1ywy56n" />\n    <bpmn2:sendTask id="Activity_0jngfnp" name="Train SVN regression algorithm">\n      <bpmn2:incoming>Flow_0slvwa6</bpmn2:incoming>\n      <bpmn2:outgoing>Flow_0m89608</bpmn2:outgoing>\n    </bpmn2:sendTask>\n    <bpmn2:textAnnotation id="TextAnnotation_0kl8mf2">\n      <bpmn2:text>regression/svn</bpmn2:text>\n    </bpmn2:textAnnotation>\n    <bpmn2:association id="Association_1h5ihkw" sourceRef="Activity_0jngfnp" targetRef="TextAnnotation_0kl8mf2" />\n  </bpmn2:process>\n  <bpmndi:BPMNDiagram id="BPMNDiagram_1">\n    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">\n      <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1">\n        <dc:Bounds x="412" y="240" width="36" height="36" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_1gzuqjq_di" bpmnElement="Activity_17z1a6q">\n        <dc:Bounds x="500" y="218" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Event_0ue1epw_di" bpmnElement="Event_0ue1epw">\n        <dc:Bounds x="982" y="240" width="36" height="36" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="979" y="283" width="43" height="14" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_1pmqlzh_di" bpmnElement="Activity_1yr2yzs">\n        <dc:Bounds x="820" y="218" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="DataObjectReference_19g0qyl_di" bpmnElement="DataObjectReference_19g0qyl">\n        <dc:Bounds x="692" y="355" width="36" height="50" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="667" y="412" width="86" height="27" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_0zgmewo_di" bpmnElement="Activity_0jngfnp">\n        <dc:Bounds x="660" y="218" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="TextAnnotation_0kl8mf2_di" bpmnElement="TextAnnotation_0kl8mf2">\n        <dc:Bounds x="760" y="130" width="110" height="41" />\n        <bpmndi:BPMNLabel />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNEdge id="Flow_0j985y1_di" bpmnElement="Flow_0j985y1">\n        <di:waypoint x="448" y="258" />\n        <di:waypoint x="500" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="DataInputAssociation_1h642dx_di" bpmnElement="DataInputAssociation_1h642dx">\n        <di:waypoint x="692" y="380" />\n        <di:waypoint x="550" y="380" />\n        <di:waypoint x="550" y="298" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_0slvwa6_di" bpmnElement="Flow_0slvwa6">\n        <di:waypoint x="600" y="258" />\n        <di:waypoint x="660" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_0m89608_di" bpmnElement="Flow_0m89608">\n        <di:waypoint x="760" y="258" />\n        <di:waypoint x="820" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_0iofx8s_di" bpmnElement="Flow_0iofx8s">\n        <di:waypoint x="920" y="258" />\n        <di:waypoint x="982" y="258" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="DataOutputAssociation_0wylqdr_di" bpmnElement="DataOutputAssociation_0wylqdr">\n        <di:waypoint x="870" y="298" />\n        <di:waypoint x="870" y="380" />\n        <di:waypoint x="728" y="380" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Association_1h5ihkw_di" bpmnElement="Association_1h5ihkw">\n        <di:waypoint x="745" y="218" />\n        <di:waypoint x="787" y="171" />\n      </bpmndi:BPMNEdge>\n    </bpmndi:BPMNPlane>\n  </bpmndi:BPMNDiagram>\n</bpmn2:definitions>\n'
    [tasks, stores] = parse_xml(raw_diagram_data["xml_original"])
    is_template = random_bool()

    return name, description, tasks, stores, raw_diagram_data, is_template


def seed_workflow(db: Session) -> dict[str, dict, WorkflowModel]:
    (
        name,
        description,
        tasks,
        stores,
        raw_diagram_data,
        is_template,
    ) = create_random_workflow(0)
    category = seed_category(db)

    workflow_in = WorkflowCreate(
        category_id=category["obj"].id,
        name=name,
        description=description,
        tasks=tasks,
        raw_diagram_data=raw_diagram_data,
        is_template=is_template,
    )
    return {
        "category_id": category["obj"].id,
        "name": name,
        "description": description,
        "tasks": tasks,
        "stores": stores,
        "raw_diagram_data": raw_diagram_data,
        "is_template": is_template,
        "obj": WorkflowController.create(db=db, obj_in=workflow_in),
    }


def update_seed_workflow(
    db: Session, workflow_id: UUID
) -> dict[str, dict, WorkflowModel]:
    (
        _,
        description,
        tasks,
        stores,
        raw_diagram_data,
        is_template,
    ) = create_random_workflow(1)

    workflow_update = WorkflowUpdate(
        description=description,
        tasks=tasks,
        raw_diagram_data=raw_diagram_data,
        is_template=is_template,
    )
    return {
        "description": description,
        "tasks": tasks,
        "stores": stores,
        "raw_diagram_data": raw_diagram_data,
        "is_template": is_template,
        "obj": WorkflowController.update(
            db=db, resource_id=workflow_id, resource_in=workflow_update
        ),
    }


def remove_workflow(db: Session, workflow_id: UUID) -> tuple[WorkflowModel | None]:
    _ = WorkflowController.destroy(
        db=db, resource_id=workflow_id, resource_in=WorkflowUpdate()
    )
    try:
        workflow_validated = WorkflowController.read(
            db=db, resource_id=workflow_id, criteria={"deleted_at": None}
        )
    except:
        workflow_validated = None

    return workflow_validated
