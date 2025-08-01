# flake8: noqa: E501
from .constants import (
    EMPTION_CHOICES,
    MAX_MSISDN_COUNT,
    MAX_PCC_RULE_COUNT,
    MAX_PRIORITY_LEVEL_VALUE,
    MAX_SESSION_NAME_LEN,
    MAX_SLICE_COUNT,
    MAX_SST_VALUE,
    MAX_SUBSCRIBER_HEX_LEN,
    MAX_SUBSCRIBER_MSISDN_LEN,
    MIN_PRIORITY_LEVEL_VALUE,
    MIN_SST_VALUE,
    QOS_INDEX_CHOICES,
    SD_LEN,
    SESSION_TYPE_CHOICES,
    UNIT_CHOICES
)
from .utils import generate_hex_key

ID_FIELD = {
    'type': 'string',
    'title': '_id',
    'pattern': '^[0-9a-fA-F]+$',
    'readOnly': True,
}

MSISDN_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'string',
        'pattern': '^\\d+$',
        'maxLength': MAX_SUBSCRIBER_MSISDN_LEN,
        'placeholder': 'Номер мобильного абонента',
    },
    'minItems': 0,
    'maxItems': MAX_MSISDN_COUNT,
    'uniqueItems': True,
    'default': [],
}

SECURITY_SCHEMA = {
    'type': 'object',
    'properties': {
        'k': {
            'type': 'string',
            'pattern': '^[0-9a-fA-F]+$',
            'title': 'Subscriber Key (K)',
            'default': generate_hex_key(MAX_SUBSCRIBER_HEX_LEN),
            'maxLength': MAX_SUBSCRIBER_HEX_LEN,
            'placeholder': '128-битный ключ в hex',
        },
        'amf': {
            'type': 'string',
            'title': 'Authentication Management Field (AMF)',
            'pattern': '^\\d+$',
            'default': '8000',
            'maxLength': MAX_SUBSCRIBER_HEX_LEN,
        },
        'op': {
            'type': 'string',
            'pattern': '^[0-9a-fA-F]+$',
            'title': 'USIM Type: OP',
            'default': None,
            'maxLength': MAX_SUBSCRIBER_HEX_LEN,
        },
        'opc': {
            'type': 'string',
            'pattern': '^[0-9a-fA-F]+$',
            'title': 'USIM Type: OPc',
            'default': None,
            'maxLength': MAX_SUBSCRIBER_HEX_LEN,
        },
    },
    'required': ['k', 'amf'],
}

AMBR_SCHEMA = {
    'type': 'object',
    'properties': {
        'downlink': {
            'type': 'object',
            'title': 'Downlink',
            'properties': {
                'value': {
                    'type': 'integer',
                    'title': 'Value',
                    'minimum': 0,
                    'placeholder': 'Макс. скорость загрузки',
                },
                'unit': {
                    'type': 'integer',
                    'title': 'Unit',
                    'enum': [choice[0] for choice in UNIT_CHOICES],
                    'default': UNIT_CHOICES[3][0],
                },
            },
            'required': ['value', 'unit']
        },
        'uplink': {
            'type': 'object',
            'title': 'Uplink',
            'properties': {
                'value': {
                    'type': 'integer',
                    'title': 'Value',
                    'minimum': 0,
                    'placeholder': 'Макс. скорость передачи',
                },
                'unit': {
                    'type': 'integer',
                    'title': 'Unit',
                    'enum': [choice[0] for choice in UNIT_CHOICES],
                    'default': UNIT_CHOICES[3][0],
                }
            },
            'required': ['value', 'unit']
        }
    },
    'required': ['downlink', 'uplink']
}

IP_CONFIG_SCHEMA = {
    'type': 'object',
    'properties': {
        'ipv4': {
            'type': 'string',
            'format': 'ipv4',
            'placeholder': 'X.X.X.X',
            'title': 'IPv4 Address',
        },
        'ipv6': {
            'type': 'string',
            'format': 'ipv6',
            'placeholder': 'XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX',
            'title': 'IPv6 Address',
        }
    },
    'additionalProperties': False
}

SESSION_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'title': 'DNN/APN',
            'maxLength': MAX_SESSION_NAME_LEN,
            'default': 'internet',
        },
        'type': {
            'type': 'integer',
            'title': 'Type',
            'enum': [choice[0] for choice in SESSION_TYPE_CHOICES],
            'default': SESSION_TYPE_CHOICES[2][0]
        },
        'qos': {
            'type': 'object',
            'title': '5QI/QCI',
            'properties': {
                'index': {
                    'type': 'integer',
                    'title': '5QI/QCI',
                    'enum': [choice[0] for choice in QOS_INDEX_CHOICES],
                    'default': QOS_INDEX_CHOICES[8][0]
                },
                'arp': {
                    'type': 'object',
                    'properties': {
                        'priority_level': {
                            'type': 'integer',
                            'title': 'ARP Priority Level',
                            'minimum': MIN_PRIORITY_LEVEL_VALUE,
                            'maximum': MAX_PRIORITY_LEVEL_VALUE,
                            'default': 8
                        },
                        'pre_emption_capability': {
                            'type': 'integer',
                            'title': 'Capability',
                            'enum': [choice[0] for choice in EMPTION_CHOICES],
                            'default': EMPTION_CHOICES[1][0]
                        },
                        'pre_emption_vulnerability': {
                            'type': 'integer',
                            'title': 'Vulnerability',
                            'enum': [choice[0] for choice in EMPTION_CHOICES],
                            'default': EMPTION_CHOICES[1][0]
                        }
                    },
                    'required': ['priority_level', 'pre_emption_capability', 'pre_emption_vulnerability']
                }
            },
            'required': ['index', 'arp']
        },
        'ambr': AMBR_SCHEMA,
        'ue': {
            **IP_CONFIG_SCHEMA,
            'title': 'UE IP Configuration',
        },
        'smf': {
            **IP_CONFIG_SCHEMA,
            'title': 'SMF IP Configuration',
        },
        'pcc_rule': {
            'type': 'array',
            'title': 'PCC Rules',
            'items': {
                'type': 'object',
                'title': 'PCC Rule',
                'properties': {
                    'qos': {
                        'type': 'object',
                        'properties': {
                            'index': {
                                'type': 'integer',
                                'title': '5QI/QCI',
                                'enum': [choice[0] for choice in QOS_INDEX_CHOICES],
                                'default': QOS_INDEX_CHOICES[0][0],
                                'placeholder': 'Индекс QoS',
                            },
                            'arp': {
                                'type': 'object',
                                'properties': {
                                    'priority_level': {
                                        'type': 'integer',
                                        'title': 'ARP Priority Level',
                                        'minimum': MIN_PRIORITY_LEVEL_VALUE,
                                        'maximum': MAX_PRIORITY_LEVEL_VALUE,
                                        'default': MIN_PRIORITY_LEVEL_VALUE + 1,
                                        'placeholder': '1 - 15',
                                    },
                                    'pre_emption_capability': {
                                        'type': 'integer',
                                        'title': 'Capability',
                                        'enum': [choice[0] for choice in EMPTION_CHOICES],
                                        'default': EMPTION_CHOICES[1][0]
                                    },
                                    'pre_emption_vulnerability': {
                                        'type': 'integer',
                                        'title': 'Vulnerability',
                                        'enum': [choice[0] for choice in EMPTION_CHOICES],
                                        'default': EMPTION_CHOICES[1][0]
                                    }
                                },
                                'required': ['priority_level', 'pre_emption_capability', 'pre_emption_vulnerability']
                            },
                            'mbr': AMBR_SCHEMA,
                            'gbr': AMBR_SCHEMA,
                        },
                        'required': ['index', 'arp']
                    },
                    '_id': ID_FIELD,
                    'flow': {
                        'type': 'array',
                        'default': [],
                        'title': 'Flow',
                        'items': {
                            'type': 'object',
                            'properties': {}
                        },
                        'readOnly': True,
                    },
                }
            },
            'default': [],
            'maxItems': MAX_PCC_RULE_COUNT
        },
        '_id': ID_FIELD,
    },
    'required': ['name', 'type', 'qos', 'ambr']
}

SLICE_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'title': 'Slice Configurations',
        'properties': {
            'sst': {
                'type': 'integer',
                'title': 'SST',
                'enum': list(range(MIN_SST_VALUE, MAX_SST_VALUE + 1)),
                'default': MIN_SST_VALUE,
            },
            'sd': {
                'type': 'string',
                'title': 'SD',
                'pattern': '^[0-9a-fA-F]*$',
                'maxLength': SD_LEN,
                'default': None
            },
            'default_indicator': {
                'type': 'boolean',
                'title': 'Default S-NSSAI',
                'default': False
            },
            'session': {
                'type': 'array',
                'title': 'Session Configurations',
                'items': SESSION_SCHEMA,
                'minItems': 1,
                'maxItems': MAX_SST_VALUE
            },
            '_id': ID_FIELD,
        },
        'required': ['sst', 'session'],
    },
    'minItems': 1,
    'maxItems': MAX_SLICE_COUNT
}