import re

from lxml import html
from typing import Dict, List, Tuple

from worker.parser.exceptions import RootMeParsingError


def is_not_participating(content: bytes) -> bool:
    tree = html.fromstring(content)
    return not tree.xpath('//div[@class="t-body tb-padding"]/div/h3[contains(.,"ne participe pas")]')


def extract_summary(content: bytes) -> Tuple[int, int, str]:
    tree = html.fromstring(content)
    success = tree.xpath('//div[@class="t-body tb-padding"]/div/p/span[2]/text()')[0]
    data = re.findall(r'(\d+)', success)
    if len(data) != 2:
        raise RootMeParsingError()
    num_success, num_try = data
    description = success.replace('\xa0', ' ').replace('\n', ' ').strip()
    return int(num_success), int(num_try), description


def extract_ctf(content: bytes) -> List[Dict[str, str]]:
    ctfs = []
    tree = html.fromstring(content)
    td_elements = tree.xpath('//table[@class="text-center mauto"]/tbody/tr')
    for td_element in td_elements:
        validated = td_element.xpath('td[1]/img/@src')[0]
        validated = re.match(r'.*/(.*?)\.png', validated).group(1)
        name = td_element.xpath('td[2]/text()')[0].replace('\xa0', '')
        num_success = td_element.xpath('td[3]/text()')[0]
        num_try = td_element.xpath('td[4]/text()')[0]
        solve_duration = td_element.xpath('td[5]/text()')[0]
        ctf = {
            'validated': validated,
            'name': name,
            'num_success': int(num_success),
            'num_try': int(num_try),
            'solve_duration': solve_duration,
        }
        ctfs.append(ctf)
    return ctfs
