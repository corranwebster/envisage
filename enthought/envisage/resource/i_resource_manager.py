""" The resource manager interface. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface

# Local imports.
from i_resource_protocol import IResourceProtocol


class IResourceManager(Interface):
    """ The resource manager interface. """

    # The protocols used by the manager to resolve resource URLs.
    resource_protocols = Instance(IResourceProtocol)
    
    def file(self, url):
        """ Return a readable file-like object for the specified url.

        Return None if the resource does not exist.

        e.g.::

          manager.file('package://acme.ui.workbench/preferences.ini')

        """

#### EOF ######################################################################
