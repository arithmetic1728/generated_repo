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

from collections import OrderedDict
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions # type: ignore
from google.api_core import exceptions                 # type: ignore
from google.api_core import gapic_v1                   # type: ignore
from google.api_core import retry as retries           # type: ignore
from google.auth import credentials                    # type: ignore
from google.oauth2 import service_account              # type: ignore

from google.container_v1.services.cluster_manager import pagers
from google.container_v1.types import cluster_service

from .transports.base import ClusterManagerTransport
from .transports.grpc import ClusterManagerGrpcTransport


class ClusterManagerClientMeta(type):
    """Metaclass for the ClusterManager client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[ClusterManagerTransport]]
    _transport_registry['grpc'] = ClusterManagerGrpcTransport

    def get_transport_class(cls,
            label: str = None,
            ) -> Type[ClusterManagerTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class ClusterManagerClient(metaclass=ClusterManagerClientMeta):
    """Google Kubernetes Engine Cluster Manager v1"""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = 'container.googleapis.com'
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(self, *,
            credentials: credentials.Credentials = None,
            transport: Union[str, ClusterManagerTransport] = None,
            client_options: ClientOptions = None,
            ) -> None:
        """Instantiate the cluster manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ClusterManagerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client.
                (2) If ``transport`` argument is None, ``client_options`` can be
                used to create a mutual TLS transport. If ``client_cert_source``
                is provided, mutual TLS transport will be created with the given
                ``api_endpoint`` or the default mTLS endpoint, and the client
                SSL credentials obtained from ``client_cert_source``.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ClusterManagerTransport):
            # transport is a ClusterManagerTransport instance.
            if credentials:
                raise ValueError('When providing a transport instance, '
                                 'provide its credentials directly.')
            self._transport = transport
        elif client_options is None or (
            client_options.api_endpoint is None
            and client_options.client_cert_source is None
        ):
            # Don't trigger mTLS if we get an empty ClientOptions.
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials, host=self.DEFAULT_ENDPOINT
            )
        else:
            # We have a non-empty ClientOptions. If client_cert_source is
            # provided, trigger mTLS with user provided endpoint or the default
            # mTLS endpoint.
            if client_options.client_cert_source:
                api_mtls_endpoint = (
                    client_options.api_endpoint
                    if client_options.api_endpoint
                    else self.DEFAULT_MTLS_ENDPOINT
                )
            else:
                api_mtls_endpoint = None

            api_endpoint = (
                client_options.api_endpoint
                if client_options.api_endpoint
                else self.DEFAULT_ENDPOINT
            )

            self._transport = ClusterManagerGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                api_mtls_endpoint=api_mtls_endpoint,
                client_cert_source=client_options.client_cert_source,
            )

    def list_clusters(self,
            request: cluster_service.ListClustersRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            parent: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.ListClustersResponse:
        r"""Lists all clusters owned by a project in either the
        specified zone or all zones.

        Args:
            request (:class:`~.cluster_service.ListClustersRequest`):
                The request object. ListClustersRequest lists clusters.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the
                parent field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides, or "-" for all zones. This
                field has been deprecated and replaced by the parent
                field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (:class:`str`):
                The parent (project and location) where the clusters
                will be listed. Specified in the format
                ``projects/*/locations/*``. Location "-" matches all
                zones and all regions.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.ListClustersResponse:
                ListClustersResponse is the result of
                ListClustersRequest.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, parent]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.ListClustersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_clusters,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_cluster(self,
            request: cluster_service.GetClusterRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Cluster:
        r"""Gets the details of a specific cluster.

        Args:
            request (:class:`~.cluster_service.GetClusterRequest`):
                The request object. GetClusterRequest gets the settings
                of a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to retrieve. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                retrieve. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Cluster:
                A Google Kubernetes Engine cluster.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.GetClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_cluster,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('name', request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_cluster(self,
            request: cluster_service.CreateClusterRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster: cluster_service.Cluster = None,
            parent: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Creates a cluster, consisting of the specified number and type
        of Google Compute Engine instances.

        By default, the cluster is created in the project's `default
        network <https://cloud.google.com/compute/docs/networks-and-firewalls#networks>`__.

        One firewall is added for the cluster. After cluster creation,
        the Kubelet creates routes for each node to allow the containers
        on that node to communicate with all other instances in the
        cluster.

        Finally, an entry is added to the project's global metadata
        indicating which CIDR range the cluster is using.

        Args:
            request (:class:`~.cluster_service.CreateClusterRequest`):
                The request object. CreateClusterRequest creates a
                cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the
                parent field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the parent field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (:class:`~.cluster_service.Cluster`):
                Required. A `cluster
                resource <https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters>`__
                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (:class:`str`):
                The parent (project and location) where the cluster will
                be created. Specified in the format
                ``projects/*/locations/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster, parent]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.CreateClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster is not None:
            request.cluster = cluster
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_cluster,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_cluster(self,
            request: cluster_service.UpdateClusterRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            update: cluster_service.ClusterUpdate = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Updates the settings of a specific cluster.

        Args:
            request (:class:`~.cluster_service.UpdateClusterRequest`):
                The request object. UpdateClusterRequest updates the
                settings of a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update (:class:`~.cluster_service.ClusterUpdate`):
                Required. A description of the
                update.
                This corresponds to the ``update`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                update. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, update, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.UpdateClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if update is not None:
            request.update = update
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_cluster,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_node_pool(self,
            request: cluster_service.UpdateNodePoolRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Updates the version and/or image type for the
        specified node pool.

        Args:
            request (:class:`~.cluster_service.UpdateNodePoolRequest`):
                The request object. UpdateNodePoolRequests update a node
                pool's image and/or version.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.UpdateNodePoolRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_node_pool,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_node_pool_autoscaling(self,
            request: cluster_service.SetNodePoolAutoscalingRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the autoscaling settings for the specified node
        pool.

        Args:
            request (:class:`~.cluster_service.SetNodePoolAutoscalingRequest`):
                The request object. SetNodePoolAutoscalingRequest sets
                the autoscaler settings of a node pool.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.SetNodePoolAutoscalingRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_node_pool_autoscaling,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_logging_service(self,
            request: cluster_service.SetLoggingServiceRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            logging_service: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the logging service for a specific cluster.

        Args:
            request (:class:`~.cluster_service.SetLoggingServiceRequest`):
                The request object. SetLoggingServiceRequest sets the
                logging service of a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            logging_service (:class:`str`):
                Required. The logging service the cluster should use to
                write metrics. Currently available options:

                -  "logging.googleapis.com" - the Google Cloud Logging
                   service
                -  "none" - no metrics will be exported from the cluster
                This corresponds to the ``logging_service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                set logging. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, logging_service, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetLoggingServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if logging_service is not None:
            request.logging_service = logging_service
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_logging_service,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_monitoring_service(self,
            request: cluster_service.SetMonitoringServiceRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            monitoring_service: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the monitoring service for a specific cluster.

        Args:
            request (:class:`~.cluster_service.SetMonitoringServiceRequest`):
                The request object. SetMonitoringServiceRequest sets the
                monitoring service of a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            monitoring_service (:class:`str`):
                Required. The monitoring service the cluster should use
                to write metrics. Currently available options:

                -  "monitoring.googleapis.com/kubernetes" - the Google
                   Cloud Monitoring service with Kubernetes-native
                   resource model
                -  "monitoring.googleapis.com" - the Google Cloud
                   Monitoring service
                -  "none" - no metrics will be exported from the cluster
                This corresponds to the ``monitoring_service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                set monitoring. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, monitoring_service, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetMonitoringServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if monitoring_service is not None:
            request.monitoring_service = monitoring_service
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_monitoring_service,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_addons_config(self,
            request: cluster_service.SetAddonsConfigRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            addons_config: cluster_service.AddonsConfig = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the addons for a specific cluster.

        Args:
            request (:class:`~.cluster_service.SetAddonsConfigRequest`):
                The request object. SetAddonsConfigRequest sets the
                addons associated with the cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            addons_config (:class:`~.cluster_service.AddonsConfig`):
                Required. The desired configurations
                for the various addons available to run
                in the cluster.
                This corresponds to the ``addons_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                set addons. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, addons_config, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetAddonsConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if addons_config is not None:
            request.addons_config = addons_config
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_addons_config,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_locations(self,
            request: cluster_service.SetLocationsRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            locations: Sequence[str] = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the locations for a specific cluster.

        Args:
            request (:class:`~.cluster_service.SetLocationsRequest`):
                The request object. SetLocationsRequest sets the
                locations of the cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            locations (:class:`Sequence[str]`):
                Required. The desired list of Google Compute Engine
                `zones <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster's nodes should be located. Changing
                the locations a cluster is in will result in nodes being
                either created or removed from the cluster, depending on
                whether locations are being added or removed.

                This list must always include the cluster's primary
                zone.
                This corresponds to the ``locations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                set locations. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, locations, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetLocationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if locations is not None:
            request.locations = locations
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_locations,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_master(self,
            request: cluster_service.UpdateMasterRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            master_version: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Updates the master for a specific cluster.

        Args:
            request (:class:`~.cluster_service.UpdateMasterRequest`):
                The request object. UpdateMasterRequest updates the
                master of the cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to upgrade. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            master_version (:class:`str`):
                Required. The Kubernetes version to
                change the master to.
                Users may specify either explicit
                versions offered by Kubernetes Engine or
                version aliases, which have the
                following behavior:
                - "latest": picks the highest valid
                Kubernetes version - "1.X": picks the
                highest valid patch+gke.N patch in the
                1.X version - "1.X.Y": picks the highest
                valid gke.N patch in the 1.X.Y version -
                "1.X.Y-gke.N": picks an explicit
                Kubernetes version - "-": picks the
                default Kubernetes version
                This corresponds to the ``master_version`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                update. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, master_version, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.UpdateMasterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if master_version is not None:
            request.master_version = master_version
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_master,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_master_auth(self,
            request: cluster_service.SetMasterAuthRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets master auth materials. Currently supports
        changing the admin password or a specific cluster,
        either via password generation or explicitly setting the
        password.

        Args:
            request (:class:`~.cluster_service.SetMasterAuthRequest`):
                The request object. SetMasterAuthRequest updates the
                admin password of a cluster.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.SetMasterAuthRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_master_auth,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_cluster(self,
            request: cluster_service.DeleteClusterRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Deletes the cluster, including the Kubernetes
        endpoint and all worker nodes.

        Firewalls and routes that were configured during cluster
        creation are also deleted.

        Other Google Compute Engine resources that might be in
        use by the cluster, such as load balancer resources, are
        not deleted if they weren't present when the cluster was
        initially created.

        Args:
            request (:class:`~.cluster_service.DeleteClusterRequest`):
                The request object. DeleteClusterRequest deletes a
                cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to delete. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster) of the cluster to
                delete. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.DeleteClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_cluster,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_operations(self,
            request: cluster_service.ListOperationsRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.ListOperationsResponse:
        r"""Lists all operations in a project in a specific zone
        or all zones.

        Args:
            request (:class:`~.cluster_service.ListOperationsRequest`):
                The request object. ListOperationsRequest lists
                operations.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the
                parent field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                to return operations for, or ``-`` for all zones. This
                field has been deprecated and replaced by the parent
                field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.ListOperationsResponse:
                ListOperationsResponse is the result
                of ListOperationsRequest.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.ListOperationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_operation(self,
            request: cluster_service.GetOperationRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            operation_id: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Gets the specified operation.

        Args:
            request (:class:`~.cluster_service.GetOperationRequest`):
                The request object. GetOperationRequest gets a single
                operation.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operation_id (:class:`str`):
                Deprecated. The server-assigned ``name`` of the
                operation. This field has been deprecated and replaced
                by the name field.
                This corresponds to the ``operation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, operation_id]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.GetOperationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if operation_id is not None:
            request.operation_id = operation_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('name', request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def cancel_operation(self,
            request: cluster_service.CancelOperationRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            operation_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Cancels the specified operation.

        Args:
            request (:class:`~.cluster_service.CancelOperationRequest`):
                The request object. CancelOperationRequest cancels a
                single operation.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the operation resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operation_id (:class:`str`):
                Deprecated. The server-assigned ``name`` of the
                operation. This field has been deprecated and replaced
                by the name field.
                This corresponds to the ``operation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, operation id) of the
                operation to cancel. Specified in the format
                ``projects/*/locations/*/operations/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, operation_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.CancelOperationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if operation_id is not None:
            request.operation_id = operation_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_server_config(self,
            request: cluster_service.GetServerConfigRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.ServerConfig:
        r"""Returns configuration info about the Google
        Kubernetes Engine service.

        Args:
            request (:class:`~.cluster_service.GetServerConfigRequest`):
                The request object. Gets the current Kubernetes Engine
                service configuration.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                to return operations for. This field has been deprecated
                and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project and location) of the server config to
                get, specified in the format ``projects/*/locations/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.ServerConfig:
                Kubernetes Engine service
                configuration.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.GetServerConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_server_config,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('name', request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_node_pools(self,
            request: cluster_service.ListNodePoolsRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            parent: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.ListNodePoolsResponse:
        r"""Lists the node pools for a cluster.

        Args:
            request (:class:`~.cluster_service.ListNodePoolsRequest`):
                The request object. ListNodePoolsRequest lists the node
                pool(s) for a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the
                parent field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the parent field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the parent field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (:class:`str`):
                The parent (project, location, cluster id) where the
                node pools will be listed. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.ListNodePoolsResponse:
                ListNodePoolsResponse is the result
                of ListNodePoolsRequest.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, parent]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.ListNodePoolsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_node_pools,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_node_pool(self,
            request: cluster_service.GetNodePoolRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            node_pool_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.NodePool:
        r"""Retrieves the requested node pool.

        Args:
            request (:class:`~.cluster_service.GetNodePoolRequest`):
                The request object. GetNodePoolRequest retrieves a node
                pool for a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool_id (:class:`str`):
                Deprecated. The name of the node
                pool. This field has been deprecated and
                replaced by the name field.
                This corresponds to the ``node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster, node pool id) of
                the node pool to get. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.NodePool:
                NodePool contains the name and
                configuration for a cluster's node pool.
                Node pools are a set of nodes (i.e.
                VM's), with a common configuration and
                specification, under the control of the
                cluster master. They may have a set of
                Kubernetes labels applied to them, which
                may be used to reference them during pod
                scheduling. They may also be resized up
                or down, to accommodate the workload.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, node_pool_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.GetNodePoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if node_pool_id is not None:
            request.node_pool_id = node_pool_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_node_pool,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('name', request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_node_pool(self,
            request: cluster_service.CreateNodePoolRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            node_pool: cluster_service.NodePool = None,
            parent: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Creates a node pool for a cluster.

        Args:
            request (:class:`~.cluster_service.CreateNodePoolRequest`):
                The request object. CreateNodePoolRequest creates a node
                pool for a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the
                parent field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the parent field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the parent field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool (:class:`~.cluster_service.NodePool`):
                Required. The node pool to create.
                This corresponds to the ``node_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (:class:`str`):
                The parent (project, location, cluster id) where the
                node pool will be created. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, node_pool, parent]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.CreateNodePoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if node_pool is not None:
            request.node_pool = node_pool
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_node_pool,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_node_pool(self,
            request: cluster_service.DeleteNodePoolRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            node_pool_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Deletes a node pool from a cluster.

        Args:
            request (:class:`~.cluster_service.DeleteNodePoolRequest`):
                The request object. DeleteNodePoolRequest deletes a node
                pool for a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool_id (:class:`str`):
                Deprecated. The name of the node pool
                to delete. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster, node pool id) of
                the node pool to delete. Specified in the format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, node_pool_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.DeleteNodePoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if node_pool_id is not None:
            request.node_pool_id = node_pool_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_node_pool,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def rollback_node_pool_upgrade(self,
            request: cluster_service.RollbackNodePoolUpgradeRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            node_pool_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Rolls back a previously Aborted or Failed NodePool
        upgrade. This makes no changes if the last upgrade
        successfully completed.

        Args:
            request (:class:`~.cluster_service.RollbackNodePoolUpgradeRequest`):
                The request object. RollbackNodePoolUpgradeRequest
                rollbacks the previously Aborted or Failed NodePool
                upgrade. This will be an no-op if the last upgrade
                successfully completed.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to rollback. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_pool_id (:class:`str`):
                Deprecated. The name of the node pool
                to rollback. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``node_pool_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster, node pool id) of
                the node poll to rollback upgrade. Specified in the
                format
                ``projects/*/locations/*/clusters/*/nodePools/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, node_pool_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.RollbackNodePoolUpgradeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if node_pool_id is not None:
            request.node_pool_id = node_pool_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.rollback_node_pool_upgrade,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_node_pool_management(self,
            request: cluster_service.SetNodePoolManagementRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the NodeManagement options for a node pool.

        Args:
            request (:class:`~.cluster_service.SetNodePoolManagementRequest`):
                The request object. SetNodePoolManagementRequest sets
                the node management properties of a node pool.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.SetNodePoolManagementRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_node_pool_management,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_labels(self,
            request: cluster_service.SetLabelsRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets labels on a cluster.

        Args:
            request (:class:`~.cluster_service.SetLabelsRequest`):
                The request object. SetLabelsRequest sets the Google
                Cloud Platform labels on a Google Container Engine
                cluster, which will in turn set them for Google Compute
                Engine resources used by that cluster

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.SetLabelsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_labels,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_legacy_abac(self,
            request: cluster_service.SetLegacyAbacRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            enabled: bool = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Enables or disables the ABAC authorization mechanism
        on a cluster.

        Args:
            request (:class:`~.cluster_service.SetLegacyAbacRequest`):
                The request object. SetLegacyAbacRequest enables or
                disables the ABAC authorization mechanism for a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster
                to update. This field has been
                deprecated and replaced by the name
                field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            enabled (:class:`bool`):
                Required. Whether ABAC authorization
                will be enabled in the cluster.
                This corresponds to the ``enabled`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster id) of the cluster
                to set legacy abac. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, enabled, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetLegacyAbacRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if enabled is not None:
            request.enabled = enabled
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_legacy_abac,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def start_ip_rotation(self,
            request: cluster_service.StartIPRotationRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Starts master IP rotation.

        Args:
            request (:class:`~.cluster_service.StartIPRotationRequest`):
                The request object. StartIPRotationRequest creates a new
                IP for the cluster and then performs a node upgrade on
                each node pool to point to the new IP.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster id) of the cluster
                to start IP rotation. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.StartIPRotationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.start_ip_rotation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def complete_ip_rotation(self,
            request: cluster_service.CompleteIPRotationRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Completes master IP rotation.

        Args:
            request (:class:`~.cluster_service.CompleteIPRotationRequest`):
                The request object. CompleteIPRotationRequest moves the
                cluster master back into single-IP mode.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster id) of the cluster
                to complete IP rotation. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.CompleteIPRotationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.complete_ip_rotation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_node_pool_size(self,
            request: cluster_service.SetNodePoolSizeRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the size for a specific node pool.

        Args:
            request (:class:`~.cluster_service.SetNodePoolSizeRequest`):
                The request object. SetNodePoolSizeRequest sets the size
                a node pool.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.SetNodePoolSizeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_node_pool_size,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_network_policy(self,
            request: cluster_service.SetNetworkPolicyRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            network_policy: cluster_service.NetworkPolicy = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Enables or disables Network Policy for a cluster.

        Args:
            request (:class:`~.cluster_service.SetNetworkPolicyRequest`):
                The request object. SetNetworkPolicyRequest
                enables/disables network policy for a cluster.
            project_id (:class:`str`):
                Deprecated. The Google Developers Console `project ID or
                project
                number <https://developers.google.com/console/help/new/#projectnumber>`__.
                This field has been deprecated and replaced by the name
                field.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Deprecated. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides. This field has been
                deprecated and replaced by the name field.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Deprecated. The name of the cluster.
                This field has been deprecated and
                replaced by the name field.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            network_policy (:class:`~.cluster_service.NetworkPolicy`):
                Required. Configuration options for
                the NetworkPolicy feature.
                This corresponds to the ``network_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster id) of the cluster
                to set networking policy. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, network_policy, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetNetworkPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if network_policy is not None:
            request.network_policy = network_policy
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_network_policy,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_maintenance_policy(self,
            request: cluster_service.SetMaintenancePolicyRequest = None,
            *,
            project_id: str = None,
            zone: str = None,
            cluster_id: str = None,
            maintenance_policy: cluster_service.MaintenancePolicy = None,
            name: str = None,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> cluster_service.Operation:
        r"""Sets the maintenance policy for a cluster.

        Args:
            request (:class:`~.cluster_service.SetMaintenancePolicyRequest`):
                The request object. SetMaintenancePolicyRequest sets the
                maintenance policy for a cluster.
            project_id (:class:`str`):
                Required. The Google Developers Console `project ID or
                project
                number <https://support.google.com/cloud/answer/6158840>`__.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            zone (:class:`str`):
                Required. The name of the Google Compute Engine
                `zone <https://cloud.google.com/compute/docs/zones#available>`__
                in which the cluster resides.
                This corresponds to the ``zone`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Required. The name of the cluster to
                update.
                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            maintenance_policy (:class:`~.cluster_service.MaintenancePolicy`):
                Required. The maintenance policy to
                be set for the cluster. An empty field
                clears the existing maintenance policy.
                This corresponds to the ``maintenance_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            name (:class:`str`):
                The name (project, location, cluster id) of the cluster
                to set maintenance policy. Specified in the format
                ``projects/*/locations/*/clusters/*``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.cluster_service.Operation:
                This operation resource represents
                operations that may have happened or are
                happening on the cluster. All fields are
                output only.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_id, zone, cluster_id, maintenance_policy, name]):
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        request = cluster_service.SetMaintenancePolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_id is not None:
            request.project_id = project_id
        if zone is not None:
            request.zone = zone
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if maintenance_policy is not None:
            request.maintenance_policy = maintenance_policy
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_maintenance_policy,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_usable_subnetworks(self,
            request: cluster_service.ListUsableSubnetworksRequest = None,
            *,
            retry: retries.Retry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListUsableSubnetworksPager:
        r"""Lists subnetworks that are usable for creating
        clusters in a project.

        Args:
            request (:class:`~.cluster_service.ListUsableSubnetworksRequest`):
                The request object. ListUsableSubnetworksRequest
                requests the list of usable subnetworks available to a
                user for creating clusters.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListUsableSubnetworksPager:
                ListUsableSubnetworksResponse is the
                response of
                ListUsableSubnetworksRequest.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.

        request = cluster_service.ListUsableSubnetworksRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_usable_subnetworks,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListUsableSubnetworksPager(
            method=rpc,
            request=request,
            response=response,
        )

        # Done; return the response.
        return response





try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            'google-container',
        ).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = (
    'ClusterManagerClient',
)
