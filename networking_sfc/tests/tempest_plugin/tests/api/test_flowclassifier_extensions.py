# Copyright 2016 Futurewei. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import six

from tempest.lib.common.utils import data_utils
from tempest import test

from networking_sfc.tests.tempest_plugin.tests.api import base


class FlowClassifierExtensionTestJSON(base.BaseFlowClassifierTest):
    """Tests the following operations in the Neutron API:

        List flowclassifiers
        Create flowclassifier
        Update flowclassifier
        Delete flowclassifier
        Show flowclassifier
    """

    @test.idempotent_id('1b84cf01-9c09-4ce7-bc72-b15e39076468')
    def test_list_flowclassifier(self):
        # List flow classifiers
        fc = self._try_create_flowclassifier()
        fcs = self.flowclassifier_client.list_flowclassifiers()
        self.assertIn((
            fc['id'],
            fc['name'],
            fc['source_ip_prefix'],
            fc['logical_source_port']
        ), [(
            m['id'],
            m['name'],
            m['source_ip_prefix'],
            m['logical_source_port'],
        ) for m in fcs['flow_classifiers']])

    @test.idempotent_id('563564f7-7077-4f5e-8cdc-51f37ae5a2b9')
    def test_update_flowclassifier(self):
        # Create flow classifier
        name1 = data_utils.rand_name('test')
        fc = self._try_create_flowclassifier(
            name=name1
        )
        fc_id = fc['id']

        # Update flow classifier
        name2 = data_utils.rand_name('test')
        body = self.flowclassifier_client.update_flowclassifier(
            fc_id, name=name2)
        self.assertEqual(body['flow_classifier']['name'], name2)

    @test.idempotent_id('3ff8c08e-26ff-4034-ae48-810ed213a998')
    def test_show_flowclassifier(self):
        # show a created flow classifier
        created = self._try_create_flowclassifier()
        fc = self.flowclassifier_client.show_flowclassifier(
            created['id'])
        for key, value in six.iteritems(fc['flow_classifier']):
            self.assertEqual(created[key], value)
