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

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.container_v1.types import cluster_service
from google.protobuf import empty_pb2 as empty  # type: ignore


class ClusterManagerTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for ClusterManager."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
    )

    def __init__(
            self, *,
            host: str = 'container.googleapis.com',
            credentials: credentials.Credentials = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def list_clusters(self) -> typing.Callable[
            [cluster_service.ListClustersRequest],
            cluster_service.ListClustersResponse]:
        raise NotImplementedError

    @property
    def get_cluster(self) -> typing.Callable[
            [cluster_service.GetClusterRequest],
            cluster_service.Cluster]:
        raise NotImplementedError

    @property
    def create_cluster(self) -> typing.Callable[
            [cluster_service.CreateClusterRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def update_cluster(self) -> typing.Callable[
            [cluster_service.UpdateClusterRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def update_node_pool(self) -> typing.Callable[
            [cluster_service.UpdateNodePoolRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_node_pool_autoscaling(self) -> typing.Callable[
            [cluster_service.SetNodePoolAutoscalingRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_logging_service(self) -> typing.Callable[
            [cluster_service.SetLoggingServiceRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_monitoring_service(self) -> typing.Callable[
            [cluster_service.SetMonitoringServiceRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_addons_config(self) -> typing.Callable[
            [cluster_service.SetAddonsConfigRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_locations(self) -> typing.Callable[
            [cluster_service.SetLocationsRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def update_master(self) -> typing.Callable[
            [cluster_service.UpdateMasterRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_master_auth(self) -> typing.Callable[
            [cluster_service.SetMasterAuthRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def delete_cluster(self) -> typing.Callable[
            [cluster_service.DeleteClusterRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def list_operations(self) -> typing.Callable[
            [cluster_service.ListOperationsRequest],
            cluster_service.ListOperationsResponse]:
        raise NotImplementedError

    @property
    def get_operation(self) -> typing.Callable[
            [cluster_service.GetOperationRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def cancel_operation(self) -> typing.Callable[
            [cluster_service.CancelOperationRequest],
            empty.Empty]:
        raise NotImplementedError

    @property
    def get_server_config(self) -> typing.Callable[
            [cluster_service.GetServerConfigRequest],
            cluster_service.ServerConfig]:
        raise NotImplementedError

    @property
    def list_node_pools(self) -> typing.Callable[
            [cluster_service.ListNodePoolsRequest],
            cluster_service.ListNodePoolsResponse]:
        raise NotImplementedError

    @property
    def get_node_pool(self) -> typing.Callable[
            [cluster_service.GetNodePoolRequest],
            cluster_service.NodePool]:
        raise NotImplementedError

    @property
    def create_node_pool(self) -> typing.Callable[
            [cluster_service.CreateNodePoolRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def delete_node_pool(self) -> typing.Callable[
            [cluster_service.DeleteNodePoolRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def rollback_node_pool_upgrade(self) -> typing.Callable[
            [cluster_service.RollbackNodePoolUpgradeRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_node_pool_management(self) -> typing.Callable[
            [cluster_service.SetNodePoolManagementRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_labels(self) -> typing.Callable[
            [cluster_service.SetLabelsRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_legacy_abac(self) -> typing.Callable[
            [cluster_service.SetLegacyAbacRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def start_ip_rotation(self) -> typing.Callable[
            [cluster_service.StartIPRotationRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def complete_ip_rotation(self) -> typing.Callable[
            [cluster_service.CompleteIPRotationRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_node_pool_size(self) -> typing.Callable[
            [cluster_service.SetNodePoolSizeRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_network_policy(self) -> typing.Callable[
            [cluster_service.SetNetworkPolicyRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def set_maintenance_policy(self) -> typing.Callable[
            [cluster_service.SetMaintenancePolicyRequest],
            cluster_service.Operation]:
        raise NotImplementedError

    @property
    def list_usable_subnetworks(self) -> typing.Callable[
            [cluster_service.ListUsableSubnetworksRequest],
            cluster_service.ListUsableSubnetworksResponse]:
        raise NotImplementedError


__all__ = (
    'ClusterManagerTransport',
)
