# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.container_v1.services.cluster_manager import ClusterManagerClient
from google.container_v1.services.cluster_manager import pagers
from google.container_v1.services.cluster_manager import transports
from google.container_v1.types import cluster_service
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert ClusterManagerClient._get_default_mtls_endpoint(None) is None
    assert ClusterManagerClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert ClusterManagerClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert ClusterManagerClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert ClusterManagerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert ClusterManagerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_cluster_manager_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = ClusterManagerClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = ClusterManagerClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == 'container.googleapis.com:443'


def test_cluster_manager_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch('google.container_v1.services.cluster_manager.ClusterManagerClient.get_transport_class') as gtc:
        transport = transports.ClusterManagerGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = ClusterManagerClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch('google.container_v1.services.cluster_manager.ClusterManagerClient.get_transport_class') as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = ClusterManagerClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch('google.container_v1.services.cluster_manager.transports.ClusterManagerGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterManagerClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check mTLS is triggered if client_cert_source is provided.
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.container_v1.services.cluster_manager.transports.ClusterManagerGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterManagerClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is triggered if api_endpoint and client_cert_source are provided.
    options = client_options.ClientOptions(
        api_endpoint="squid.clam.whelk",
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.container_v1.services.cluster_manager.transports.ClusterManagerGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterManagerClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )

def test_cluster_manager_client_client_options_from_dict():
    with mock.patch('google.container_v1.services.cluster_manager.transports.ClusterManagerGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = ClusterManagerClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_list_clusters(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.ListClustersRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_clusters),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse(
            missing_zones=['missing_zones_value'],
        )

        response = client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListClustersResponse)
    assert response.missing_zones == ['missing_zones_value']


def test_list_clusters_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListClustersRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_clusters),
            '__call__') as call:
        call.return_value = cluster_service.ListClustersResponse()
        client.list_clusters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_clusters_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_clusters),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListClustersResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_clusters(
            project_id='project_id_value',
            zone='zone_value',
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].parent == 'parent_value'


def test_list_clusters_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_clusters(
            cluster_service.ListClustersRequest(),
            project_id='project_id_value',
            zone='zone_value',
            parent='parent_value',
        )


def test_get_cluster(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.GetClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster(
            name='name_value',
            description='description_value',
            initial_node_count=1911,
            logging_service='logging_service_value',
            monitoring_service='monitoring_service_value',
            network='network_value',
            cluster_ipv4_cidr='cluster_ipv4_cidr_value',
            subnetwork='subnetwork_value',
            locations=['locations_value'],
            enable_kubernetes_alpha=True,
            label_fingerprint='label_fingerprint_value',
            self_link='self_link_value',
            zone='zone_value',
            endpoint='endpoint_value',
            initial_cluster_version='initial_cluster_version_value',
            current_master_version='current_master_version_value',
            current_node_version='current_node_version_value',
            create_time='create_time_value',
            status=cluster_service.Cluster.Status.PROVISIONING,
            status_message='status_message_value',
            node_ipv4_cidr_size=1955,
            services_ipv4_cidr='services_ipv4_cidr_value',
            instance_group_urls=['instance_group_urls_value'],
            current_node_count=1936,
            expire_time='expire_time_value',
            location='location_value',
            enable_tpu=True,
            tpu_ipv4_cidr_block='tpu_ipv4_cidr_block_value',
        )

        response = client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Cluster)
    assert response.name == 'name_value'
    assert response.description == 'description_value'
    assert response.initial_node_count == 1911
    assert response.logging_service == 'logging_service_value'
    assert response.monitoring_service == 'monitoring_service_value'
    assert response.network == 'network_value'
    assert response.cluster_ipv4_cidr == 'cluster_ipv4_cidr_value'
    assert response.subnetwork == 'subnetwork_value'
    assert response.locations == ['locations_value']

    assert response.enable_kubernetes_alpha is True
    assert response.label_fingerprint == 'label_fingerprint_value'
    assert response.self_link == 'self_link_value'
    assert response.zone == 'zone_value'
    assert response.endpoint == 'endpoint_value'
    assert response.initial_cluster_version == 'initial_cluster_version_value'
    assert response.current_master_version == 'current_master_version_value'
    assert response.current_node_version == 'current_node_version_value'
    assert response.create_time == 'create_time_value'
    assert response.status == cluster_service.Cluster.Status.PROVISIONING
    assert response.status_message == 'status_message_value'
    assert response.node_ipv4_cidr_size == 1955
    assert response.services_ipv4_cidr == 'services_ipv4_cidr_value'
    assert response.instance_group_urls == ['instance_group_urls_value']
    assert response.current_node_count == 1936
    assert response.expire_time == 'expire_time_value'
    assert response.location == 'location_value'

    assert response.enable_tpu is True
    assert response.tpu_ipv4_cidr_block == 'tpu_ipv4_cidr_block_value'


def test_get_cluster_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetClusterRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_cluster),
            '__call__') as call:
        call.return_value = cluster_service.Cluster()
        client.get_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_cluster_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Cluster()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_cluster(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].name == 'name_value'


def test_get_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_cluster(
            cluster_service.GetClusterRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )


def test_create_cluster(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.CreateClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.create_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_create_cluster_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_cluster(
            project_id='project_id_value',
            zone='zone_value',
            cluster=cluster_service.Cluster(name='name_value'),
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster == cluster_service.Cluster(name='name_value')
        assert args[0].parent == 'parent_value'


def test_create_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_cluster(
            cluster_service.CreateClusterRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster=cluster_service.Cluster(name='name_value'),
            parent='parent_value',
        )


def test_update_cluster(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.UpdateClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.update_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_update_cluster_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_cluster(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            update=cluster_service.ClusterUpdate(desired_node_version='desired_node_version_value'),
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].update == cluster_service.ClusterUpdate(desired_node_version='desired_node_version_value')
        assert args[0].name == 'name_value'


def test_update_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_cluster(
            cluster_service.UpdateClusterRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            update=cluster_service.ClusterUpdate(desired_node_version='desired_node_version_value'),
            name='name_value',
        )


def test_update_node_pool(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.UpdateNodePoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.update_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_node_pool_autoscaling(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetNodePoolAutoscalingRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_node_pool_autoscaling),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_node_pool_autoscaling(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_logging_service(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetLoggingServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_logging_service),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_logging_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_logging_service_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_logging_service),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_logging_service(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            logging_service='logging_service_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].logging_service == 'logging_service_value'
        assert args[0].name == 'name_value'


def test_set_logging_service_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_logging_service(
            cluster_service.SetLoggingServiceRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            logging_service='logging_service_value',
            name='name_value',
        )


def test_set_monitoring_service(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetMonitoringServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_monitoring_service),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_monitoring_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_monitoring_service_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_monitoring_service),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_monitoring_service(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            monitoring_service='monitoring_service_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].monitoring_service == 'monitoring_service_value'
        assert args[0].name == 'name_value'


def test_set_monitoring_service_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_monitoring_service(
            cluster_service.SetMonitoringServiceRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            monitoring_service='monitoring_service_value',
            name='name_value',
        )


def test_set_addons_config(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetAddonsConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_addons_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_addons_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_addons_config_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_addons_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_addons_config(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            addons_config=cluster_service.AddonsConfig(http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)),
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].addons_config == cluster_service.AddonsConfig(http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True))
        assert args[0].name == 'name_value'


def test_set_addons_config_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_addons_config(
            cluster_service.SetAddonsConfigRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            addons_config=cluster_service.AddonsConfig(http_load_balancing=cluster_service.HttpLoadBalancing(disabled=True)),
            name='name_value',
        )


def test_set_locations(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetLocationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_locations),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_locations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_locations_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_locations),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_locations(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            locations=['locations_value'],
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].locations == ['locations_value']
        assert args[0].name == 'name_value'


def test_set_locations_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_locations(
            cluster_service.SetLocationsRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            locations=['locations_value'],
            name='name_value',
        )


def test_update_master(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.UpdateMasterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_master),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.update_master(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_update_master_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_master),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_master(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            master_version='master_version_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].master_version == 'master_version_value'
        assert args[0].name == 'name_value'


def test_update_master_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_master(
            cluster_service.UpdateMasterRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            master_version='master_version_value',
            name='name_value',
        )


def test_set_master_auth(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetMasterAuthRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_master_auth),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_master_auth(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_delete_cluster(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.DeleteClusterRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.delete_cluster(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_delete_cluster_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_cluster),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_cluster(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].name == 'name_value'


def test_delete_cluster_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_cluster(
            cluster_service.DeleteClusterRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )


def test_list_operations(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_operations),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse(
            missing_zones=['missing_zones_value'],
        )

        response = client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListOperationsResponse)
    assert response.missing_zones == ['missing_zones_value']


def test_list_operations_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListOperationsRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_operations),
            '__call__') as call:
        call.return_value = cluster_service.ListOperationsResponse()
        client.list_operations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_operations_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_operations),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListOperationsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_operations(
            project_id='project_id_value',
            zone='zone_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'


def test_list_operations_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_operations(
            cluster_service.ListOperationsRequest(),
            project_id='project_id_value',
            zone='zone_value',
        )


def test_get_operation(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_operation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_get_operation_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetOperationRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_operation),
            '__call__') as call:
        call.return_value = cluster_service.Operation()
        client.get_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_operation_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_operation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_operation(
            project_id='project_id_value',
            zone='zone_value',
            operation_id='operation_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].operation_id == 'operation_id_value'


def test_get_operation_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_operation(
            cluster_service.GetOperationRequest(),
            project_id='project_id_value',
            zone='zone_value',
            operation_id='operation_id_value',
        )


def test_cancel_operation(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.cancel_operation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.cancel_operation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.cancel_operation(
            project_id='project_id_value',
            zone='zone_value',
            operation_id='operation_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].operation_id == 'operation_id_value'
        assert args[0].name == 'name_value'


def test_cancel_operation_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.cancel_operation(
            cluster_service.CancelOperationRequest(),
            project_id='project_id_value',
            zone='zone_value',
            operation_id='operation_id_value',
            name='name_value',
        )


def test_get_server_config(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.GetServerConfigRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_server_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig(
            default_cluster_version='default_cluster_version_value',
            valid_node_versions=['valid_node_versions_value'],
            default_image_type='default_image_type_value',
            valid_image_types=['valid_image_types_value'],
            valid_master_versions=['valid_master_versions_value'],
        )

        response = client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ServerConfig)
    assert response.default_cluster_version == 'default_cluster_version_value'
    assert response.valid_node_versions == ['valid_node_versions_value']
    assert response.default_image_type == 'default_image_type_value'
    assert response.valid_image_types == ['valid_image_types_value']
    assert response.valid_master_versions == ['valid_master_versions_value']


def test_get_server_config_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetServerConfigRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_server_config),
            '__call__') as call:
        call.return_value = cluster_service.ServerConfig()
        client.get_server_config(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_server_config_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_server_config),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ServerConfig()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_server_config(
            project_id='project_id_value',
            zone='zone_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].name == 'name_value'


def test_get_server_config_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_server_config(
            cluster_service.GetServerConfigRequest(),
            project_id='project_id_value',
            zone='zone_value',
            name='name_value',
        )


def test_list_node_pools(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.ListNodePoolsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_node_pools),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse(
        )

        response = client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.ListNodePoolsResponse)


def test_list_node_pools_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListNodePoolsRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_node_pools),
            '__call__') as call:
        call.return_value = cluster_service.ListNodePoolsResponse()
        client.list_node_pools(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_node_pools_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_node_pools),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListNodePoolsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_node_pools(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].parent == 'parent_value'


def test_list_node_pools_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_node_pools(
            cluster_service.ListNodePoolsRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            parent='parent_value',
        )


def test_get_node_pool(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.GetNodePoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool(
            name='name_value',
            initial_node_count=1911,
            self_link='self_link_value',
            version='version_value',
            instance_group_urls=['instance_group_urls_value'],
            status=cluster_service.NodePool.Status.PROVISIONING,
            status_message='status_message_value',
            pod_ipv4_cidr_size=1856,
        )

        response = client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.NodePool)
    assert response.name == 'name_value'
    assert response.initial_node_count == 1911
    assert response.self_link == 'self_link_value'
    assert response.version == 'version_value'
    assert response.instance_group_urls == ['instance_group_urls_value']
    assert response.status == cluster_service.NodePool.Status.PROVISIONING
    assert response.status_message == 'status_message_value'
    assert response.pod_ipv4_cidr_size == 1856


def test_get_node_pool_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.GetNodePoolRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_node_pool),
            '__call__') as call:
        call.return_value = cluster_service.NodePool()
        client.get_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_node_pool_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.NodePool()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_node_pool(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool_id='node_pool_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].node_pool_id == 'node_pool_id_value'
        assert args[0].name == 'name_value'


def test_get_node_pool_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_node_pool(
            cluster_service.GetNodePoolRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool_id='node_pool_id_value',
            name='name_value',
        )


def test_create_node_pool(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.CreateNodePoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.create_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_create_node_pool_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_node_pool(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool=cluster_service.NodePool(name='name_value'),
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].node_pool == cluster_service.NodePool(name='name_value')
        assert args[0].parent == 'parent_value'


def test_create_node_pool_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_node_pool(
            cluster_service.CreateNodePoolRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool=cluster_service.NodePool(name='name_value'),
            parent='parent_value',
        )


def test_delete_node_pool(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.DeleteNodePoolRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.delete_node_pool(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_delete_node_pool_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.delete_node_pool),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_node_pool(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool_id='node_pool_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].node_pool_id == 'node_pool_id_value'
        assert args[0].name == 'name_value'


def test_delete_node_pool_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_node_pool(
            cluster_service.DeleteNodePoolRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool_id='node_pool_id_value',
            name='name_value',
        )


def test_rollback_node_pool_upgrade(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.RollbackNodePoolUpgradeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.rollback_node_pool_upgrade),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.rollback_node_pool_upgrade(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_rollback_node_pool_upgrade_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.rollback_node_pool_upgrade),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.rollback_node_pool_upgrade(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool_id='node_pool_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].node_pool_id == 'node_pool_id_value'
        assert args[0].name == 'name_value'


def test_rollback_node_pool_upgrade_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.rollback_node_pool_upgrade(
            cluster_service.RollbackNodePoolUpgradeRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            node_pool_id='node_pool_id_value',
            name='name_value',
        )


def test_set_node_pool_management(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetNodePoolManagementRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_node_pool_management),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_node_pool_management(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_labels(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetLabelsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_labels),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_labels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_legacy_abac(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetLegacyAbacRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_legacy_abac),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_legacy_abac(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_legacy_abac_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_legacy_abac),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_legacy_abac(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            enabled=True,
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].enabled == True
        assert args[0].name == 'name_value'


def test_set_legacy_abac_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_legacy_abac(
            cluster_service.SetLegacyAbacRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            enabled=True,
            name='name_value',
        )


def test_start_ip_rotation(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.StartIPRotationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.start_ip_rotation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.start_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_start_ip_rotation_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.start_ip_rotation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.start_ip_rotation(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].name == 'name_value'


def test_start_ip_rotation_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_ip_rotation(
            cluster_service.StartIPRotationRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )


def test_complete_ip_rotation(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.CompleteIPRotationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.complete_ip_rotation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.complete_ip_rotation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_complete_ip_rotation_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.complete_ip_rotation),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.complete_ip_rotation(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].name == 'name_value'


def test_complete_ip_rotation_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.complete_ip_rotation(
            cluster_service.CompleteIPRotationRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            name='name_value',
        )


def test_set_node_pool_size(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetNodePoolSizeRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_node_pool_size),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_node_pool_size(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_network_policy(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetNetworkPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_network_policy),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_network_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_network_policy_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_network_policy),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_network_policy(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            network_policy=cluster_service.NetworkPolicy(provider=cluster_service.NetworkPolicy.Provider.CALICO),
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].network_policy == cluster_service.NetworkPolicy(provider=cluster_service.NetworkPolicy.Provider.CALICO)
        assert args[0].name == 'name_value'


def test_set_network_policy_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_network_policy(
            cluster_service.SetNetworkPolicyRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            network_policy=cluster_service.NetworkPolicy(provider=cluster_service.NetworkPolicy.Provider.CALICO),
            name='name_value',
        )


def test_set_maintenance_policy(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.SetMaintenancePolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_maintenance_policy),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation(
            name='name_value',
            zone='zone_value',
            operation_type=cluster_service.Operation.Type.CREATE_CLUSTER,
            status=cluster_service.Operation.Status.PENDING,
            detail='detail_value',
            status_message='status_message_value',
            self_link='self_link_value',
            target_link='target_link_value',
            location='location_value',
            start_time='start_time_value',
            end_time='end_time_value',
        )

        response = client.set_maintenance_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cluster_service.Operation)
    assert response.name == 'name_value'
    assert response.zone == 'zone_value'
    assert response.operation_type == cluster_service.Operation.Type.CREATE_CLUSTER
    assert response.status == cluster_service.Operation.Status.PENDING
    assert response.detail == 'detail_value'
    assert response.status_message == 'status_message_value'
    assert response.self_link == 'self_link_value'
    assert response.target_link == 'target_link_value'
    assert response.location == 'location_value'
    assert response.start_time == 'start_time_value'
    assert response.end_time == 'end_time_value'


def test_set_maintenance_policy_flattened():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.set_maintenance_policy),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.Operation()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_maintenance_policy(
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            maintenance_policy=cluster_service.MaintenancePolicy(window=cluster_service.MaintenanceWindow(daily_maintenance_window=cluster_service.DailyMaintenanceWindow(start_time='start_time_value'))),
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].project_id == 'project_id_value'
        assert args[0].zone == 'zone_value'
        assert args[0].cluster_id == 'cluster_id_value'
        assert args[0].maintenance_policy == cluster_service.MaintenancePolicy(window=cluster_service.MaintenanceWindow(daily_maintenance_window=cluster_service.DailyMaintenanceWindow(start_time='start_time_value')))
        assert args[0].name == 'name_value'


def test_set_maintenance_policy_flattened_error():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_maintenance_policy(
            cluster_service.SetMaintenancePolicyRequest(),
            project_id='project_id_value',
            zone='zone_value',
            cluster_id='cluster_id_value',
            maintenance_policy=cluster_service.MaintenancePolicy(window=cluster_service.MaintenanceWindow(daily_maintenance_window=cluster_service.DailyMaintenanceWindow(start_time='start_time_value'))),
            name='name_value',
        )


def test_list_usable_subnetworks(transport: str = 'grpc'):
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cluster_service.ListUsableSubnetworksRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_usable_subnetworks),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = cluster_service.ListUsableSubnetworksResponse(
            next_page_token='next_page_token_value',
        )

        response = client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUsableSubnetworksPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_usable_subnetworks_field_headers():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cluster_service.ListUsableSubnetworksRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_usable_subnetworks),
            '__call__') as call:
        call.return_value = cluster_service.ListUsableSubnetworksResponse()
        client.list_usable_subnetworks(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_usable_subnetworks_pager():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_usable_subnetworks),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token='abc',
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[],
                next_page_token='def',
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token='ghi',
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_usable_subnetworks(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, cluster_service.UsableSubnetwork)
                   for i in results)

def test_list_usable_subnetworks_pages():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_usable_subnetworks),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token='abc',
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[],
                next_page_token='def',
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                ],
                next_page_token='ghi',
            ),
            cluster_service.ListUsableSubnetworksResponse(
                subnetworks=[
                    cluster_service.UsableSubnetwork(),
                    cluster_service.UsableSubnetwork(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_usable_subnetworks(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ClusterManagerClient(
            credentials=credentials.AnonymousCredentials(),
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ClusterManagerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ClusterManagerClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client._transport,
        transports.ClusterManagerGrpcTransport,
    )


def test_cluster_manager_base_transport():
    # Instantiate the base transport.
    transport = transports.ClusterManagerTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'list_clusters',
        'get_cluster',
        'create_cluster',
        'update_cluster',
        'update_node_pool',
        'set_node_pool_autoscaling',
        'set_logging_service',
        'set_monitoring_service',
        'set_addons_config',
        'set_locations',
        'update_master',
        'set_master_auth',
        'delete_cluster',
        'list_operations',
        'get_operation',
        'cancel_operation',
        'get_server_config',
        'list_node_pools',
        'get_node_pool',
        'create_node_pool',
        'delete_node_pool',
        'rollback_node_pool_upgrade',
        'set_node_pool_management',
        'set_labels',
        'set_legacy_abac',
        'start_ip_rotation',
        'complete_ip_rotation',
        'set_node_pool_size',
        'set_network_policy',
        'set_maintenance_policy',
        'list_usable_subnetworks',
        )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_cluster_manager_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, 'default') as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ClusterManagerClient()
        adc.assert_called_once_with(scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
        ))


def test_cluster_manager_host_no_port():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='container.googleapis.com'),
        transport='grpc',
    )
    assert client._transport._host == 'container.googleapis.com:443'


def test_cluster_manager_host_with_port():
    client = ClusterManagerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='container.googleapis.com:8000'),
        transport='grpc',
    )
    assert client._transport._host == 'container.googleapis.com:8000'


def test_cluster_manager_grpc_transport_channel():
    channel = grpc.insecure_channel('http://localhost/')

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.ClusterManagerGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_cluster_manager_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.ClusterManagerGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
        ),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_cluster_manager_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.ClusterManagerGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
            ),
        )
        assert transport.grpc_channel == mock_grpc_channel
