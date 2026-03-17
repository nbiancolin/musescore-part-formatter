from dataclasses import dataclass
import xml.etree.ElementTree as ET

@dataclass
class TitleBoxProperties:

    title: str
    subtitle: str

    conposer: str
    lyricist: str

    part_name: str

    custom_fields: dict[str, str]


    def get(self, key: str) -> str | None:
        if value := getattr(self, key, None):
            return value

        return self.custom_fields.get(key)

def get_title_box_properties(score: ET.Element) -> TitleBoxProperties:
    pass


def _set_title_box_property(score: ET.Element, prop: str, value: str):
    pass


def set_title_box_properties(score: ET.Element, props: TitleBoxProperties):
    existing_meta = score.findall("metaTag")

    if existing_meta:
        insert_index = list(score).index(existing_meta[-1]) + 1
    else:
        insert_index = 0

    for k, v in props.items():
        tag = score.find(f"metaTag[@name='{k}']")

        if tag is not None:
            tag.text = v
        else:
            new_tag = ET.Element("metaTag")
            new_tag.set("name", k)
            new_tag.text = v
            score.insert(insert_index, new_tag)
            insert_index += 1   # keep new metaTags grouped together


