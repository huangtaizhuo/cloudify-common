# flake8: NOQA
########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'ran'

ADVANCED_OPERATION_MAPPING_SCHEMA = {
    'type': 'object',
    'properties': {
        'mapping': {
            'type': 'string'
        },
        'properties': {
            'type': 'object',
            'minProperties': 1
        }
    },
    'required': ['mapping', 'properties'],
    'additionalProperties': False
}

INTERFACES_SCHEMA = {
    'type': 'object',
    'patternProperties': {
        '^': {
            'type': 'array',
            'items': {
                'oneOf': [
                    {
                        'type': 'string'
                    },
                    {
                        'type': 'object',
                        'patternProperties': {
                            '^': {
                                'oneOf': [
                                    {'type': 'string'},
                                    ADVANCED_OPERATION_MAPPING_SCHEMA,
                                ]
                            }
                        },
                        'maxProperties': 1,
                        'minProperties': 1
                    }
                ]
            },
            'uniqueItems': True,
            'minItems': 1
        }
    },
    'minProperties': 1
}

PROPERTIES_SCHEMA_SCHEMA = {
    'type': 'object',
    'patternProperties': {
        '^': {
            # can't seem to be able to do the 'oneOf' inside the
            # 'properties' object, so some duplication is required here in
            # order to allow any type for the 'default' value.
            'anyOf': [
                {
                    'type': 'object',
                    'properties': {
                        'default': {
                            'type': 'object'
                        },
                        'description': {
                            'type': 'string'
                        }
                    },
                    'additionalProperties': False
                },
                {
                    'type': 'object',
                    'properties': {
                        'default': {
                            'type': 'string'
                        },
                        'description': {
                            'type': 'string'
                        }
                    },
                    'additionalProperties': False
                },
                {
                    'type': 'object',
                    'properties': {
                        'default': {
                            'type': 'number'
                        },
                        'description': {
                            'type': 'string'
                        }
                    },
                    'additionalProperties': False
                },
                {
                    'type': 'object',
                    'properties': {
                        'default': {
                            'type': 'boolean'
                        },
                        'description': {
                            'type': 'string'
                        }
                    },
                    'additionalProperties': False
                },
                {
                    'type': 'object',
                    'properties': {
                        'default': {
                            'type': 'array'
                        },
                        'description': {
                            'type': 'string'
                        }
                    },
                    'additionalProperties': False
                }
            ]
        }
    }
}

WORKFLOW_MAPPING_SCHEMA = {
    'type': 'object',
    'properties': {
        'mapping': {
            'type': 'string'
        },
        'parameters': PROPERTIES_SCHEMA_SCHEMA,
    },
    'required': ['mapping', 'parameters'],
    'additionalProperties': False
}

WORKFLOWS_SCHEMA = {
    'type': 'object',
    'patternProperties': {
        '^': {
            'oneOf': [
                {'type': 'string'},
                WORKFLOW_MAPPING_SCHEMA,
            ]
        },
    }
}

UNIQUE_STRING_ARRAY_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'string'
    },
    'uniqueItems': True
}

IMPORTS_SCHEMA = UNIQUE_STRING_ARRAY_SCHEMA

MEMBERS_SCHEMA = UNIQUE_STRING_ARRAY_SCHEMA.copy()
MEMBERS_SCHEMA['minItems'] = 1

# Schema validation is currently done using a json schema validator
# ( see http://json-schema.org/ ), since no good YAML schema validator could
# be found (both for Python and at all).
#
# Python implementation documentation:
# http://python-jsonschema.readthedocs.org/en/latest/
# A one-stop-shop for easy API explanation:
# http://jsonary.com/documentation/json-schema/?
# A website which can create a schema from a given JSON automatically:
# http://www.jsonschema.net/#
# (Note: the website was not used for creating the schema below, as among
# other things, its syntax seems a bit different than the one used here,
# and should only be used as a reference)
DSL_SCHEMA = {
    'type': 'object',
    'properties': {
        'node_templates': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        #non-meta 'type'
                        'type': {
                            'type': 'string'
                        },
                        'instances': {
                            'type': 'object',
                            'properties': {
                                'deploy': {
                                    'type': 'number'
                                }
                            },
                            'required': ['deploy'],
                            'additionalProperties': False
                        },
                        'interfaces': INTERFACES_SCHEMA,
                        'relationships': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    #non-meta 'type'
                                    'type': {
                                        'type': 'string'
                                    },
                                    'target': {
                                        'type': 'string'
                                    },
                                    #non-meta 'properties'
                                    'properties': {
                                        'type': 'object'
                                    },
                                    'source_interfaces': INTERFACES_SCHEMA,
                                    'target_interfaces': INTERFACES_SCHEMA,
                                },
                                'required': ['type', 'target'],
                                'additionalProperties': False
                            }
                        },
                        #non-meta 'properties'
                        'properties': {
                            'type': 'object'
                        }
                    },
                    'required': ['type'],
                    'additionalProperties': False
                }
            }
        },
        'plugins': {
            'type': 'object',
            'patternProperties': {
                #this is specifically for the root plugin, not meant for other uses
                '^cloudify.plugins.plugin$': {
                    'type': 'object',
                    'properties': {},
                    'additionalProperties': False
                },
                '^((?!cloudify\.plugins\.plugin).*)$|^cloudify\.plugins\.plugin.+$': {
                    'type': 'object',
                    'properties': {
                        'derived_from': {
                            'type': 'string'
                        },
                        #non-meta 'properties'
                        'properties': {
                            'type': 'object',
                            'oneOf': [
                                {
                                    'properties': {
                                        'url': {
                                            'type': 'string'
                                        }
                                    },
                                    'required': ['url'],
                                    'additionalProperties': False
                                },
                                {
                                    'properties': {
                                        'folder': {
                                            'type': 'string'
                                        }
                                    },
                                    'required': ['folder'],
                                    'additionalProperties': False
                                }
                            ]
                        }
                    },
                    'required': ['derived_from'],
                    'additionalProperties': False
                }
            },
            'additionalProperties': False
        },
        'policy_types': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        'properties': PROPERTIES_SCHEMA_SCHEMA,
                        'source': {
                            'type': 'string'
                        }
                    },
                    'required': ['properties', 'source'],
                    'additionalProperties': False
                },
            },
            'additionalProperties': False
        },
        'groups': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        'members': MEMBERS_SCHEMA,
                        'policies': {
                            'type': 'object',
                            'patternProperties': {
                                '^': {
                                    'type': 'object',
                                    'properties': {
                                        #non-meta 'properties'
                                        'type': {
                                            'type': 'string'
                                        },
                                        'properties': {
                                            'type': 'object'
                                        }
                                    },
                                    'required': ['type', 'properties'],
                                    'additionalProperties': False
                                },
                            },
                            'additionalProperties': False
                        }
                    },
                    'required': ['policies', 'members'],
                    'additionalProperties': False
                },
            },
            'additionalProperties': False
        },
        'node_types': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        'interfaces': INTERFACES_SCHEMA,
                        #non-meta 'properties'
                        'properties': PROPERTIES_SCHEMA_SCHEMA,
                        'derived_from': {
                            'type': 'string'
                        },
                    },
                    'additionalProperties': False
                }
            }
        },
        'type_implementations': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        #non-meta 'properties'
                        'properties': {
                            'type': 'object'
                        },
                        'type': {
                            'type': 'string'
                        },
                        'node_ref': {
                            'type': 'string'
                        },
                    },
                    'required': ['node_ref', 'type'],
                    'additionalProperties': False
                }
            }
        },
        'workflows': WORKFLOWS_SCHEMA,
        'relationships': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        'derived_from': {
                            'type': 'string'
                        },
                        'source_interfaces': INTERFACES_SCHEMA,
                        'target_interfaces': INTERFACES_SCHEMA,
                        #non-meta 'properties'
                        'properties': PROPERTIES_SCHEMA_SCHEMA
                    },
                    'additionalProperties': False
                }
            }
        },
        'relationship_implementations': {
            'type': 'object',
            'patternProperties': {
                '^': {
                    'type': 'object',
                    'properties': {
                        'type': {
                            'type': 'string'
                        },
                        'source_node_ref': {
                            'type': 'string'
                        },
                        'target_node_ref': {
                            'type': 'string'
                        },
                        #non-meta 'properties'
                        'properties': {
                            'type': 'object'
                        },
                    },
                    'required': ['source_node_ref', 'target_node_ref',
                                 'type'],
                    'additionalProperties': False
                }
            }
        },
    },
    'required': ['node_templates'],
    'additionalProperties': False
}
