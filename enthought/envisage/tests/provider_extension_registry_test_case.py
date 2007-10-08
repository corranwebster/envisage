""" Tests for the provider extension registry. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, ExtensionProvider
from enthought.envisage.api import ProviderExtensionRegistry
from enthought.traits.api import Int, List    

# Local imports.
from extension_registry_test_case import ExtensionRegistryTestCase


class ProviderExtensionTestCase(ExtensionRegistryTestCase):
    """ Tests for the provider extension registry. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        self.registry = ProviderExtensionRegistry()

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################
    
    def test_providers(self):
        """ providers """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """
                
                return [ExtensionPoint(List, 'x')]
            
            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [42, 43]

                else:
                    extensions = []

                return extensions

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [44, 45, 46]

                else:
                    extensions = []

                return extensions

        # Add the providers to the registry.
        registry.add_providers([ProviderA(), ProviderB()])

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(5, len(extensions))
        self.assertEqual(range(42, 47), extensions)

        # Make sure there's one and only one extension point.
        extension_points = registry.get_extension_points()
        self.assertEqual(1, len(extension_points))
        self.assertEqual('x', extension_points[0])

        return

    def test_provider_extensions_changed(self):
        """ provider extensions changed """

        registry = self.registry

        # A provider.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            x = List(Int)
            
            def get_extension_points(self):
                """ Return the extension points offered by the provider. """
                
                return [ExtensionPoint(List, 'x')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'my.ep':
                    return self.x

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'my.ep', event.added, event.removed, event.index
                )
                
                return

        # Add the provider to the registry.
        a = ProviderA(x=[42])
        registry.add_provider(a)

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed
            listener.index = event.index

            return

        registry.add_extension_listener(listener, 'my.ep')
        
        # Add a new extension via the provider.
        a.x.append(43)

        # Make sure the listener got called.
        self.assertEqual('my.ep', listener.extension_point)
        self.assertEqual([43], listener.added)
        self.assertEqual([], listener.removed)
        
        # Now we should get the new extension.
        extensions = registry.get_extensions('my.ep')
        self.assertEqual(2, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)

        return

    def test_add_provider(self):
        """ add provider """

        registry = self.registry

        # A provider.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extension_points(self):
                """ Return the extension points offered by the provider. """
                
                return [ExtensionPoint(List, 'x')]

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    return [42]

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'x', event.added, event.removed, event.index
                )
                
                return

        # Add the provider to the registry.
        registry.add_provider(ProviderA())

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed
            listener.index = event.index

            return

        registry.add_extension_listener(listener, 'x')

        # Add a new provider.
        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        registry.add_provider(ProviderB())

        # Make sure the listener got called.
        self.assertEqual('x', listener.extension_point)
        self.assertEqual([43, 44], listener.added)
        self.assertEqual([], listener.removed)
        
        # Now we should get the new extensions.
        extensions = registry.get_extensions('x')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        return

    def test_remove_provider(self):
        """ remove provider """

        registry = self.registry

        # Some providers.
        class ProviderA(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    return [42]

                else:
                    extensions = []

                return extensions

            def _x_items_changed(self, event):
                """ Static trait change handler. """

                self._fire_extension_point_changed(
                    'x', event.added, event.removed, event.index
                )
                
                return

        class ProviderB(ExtensionProvider):
            """ An extension provider. """

            def get_extensions(self, extension_point):
                """ Return the provider's contributions to an extension point.

                """

                if extension_point == 'x':
                    extensions = [43, 44]

                else:
                    extensions = []

                return extensions

        # Add the providers to the registry.
        a = ProviderA()
        b = ProviderB()
        registry.add_providers([a, b])

        # The provider's extensions should now be in the registry.
        extensions = registry.get_extensions('x')
        self.assertEqual(3, len(extensions))
        self.assert_(42 in extensions)
        self.assert_(43 in extensions)
        self.assert_(44 in extensions)

        # Add an extension listener to the registry.
        def listener(registry, event):
            """ A useful trait change handler for testing! """

            listener.registry = registry
            listener.extension_point = event.extension_point_id
            listener.added = event.added
            listener.removed = event.removed

            return

        registry.add_extension_listener(listener, 'x')

        # Remove one of the providers.
        registry.remove_provider(b)

        # Make sure the listener got called.
        self.assertEqual('x', listener.extension_point)
        self.assertEqual([], listener.added)
        self.assertEqual([43, 44], listener.removed)
        
        # Make sure we don't get the removed extensions.
        extensions = registry.get_extensions('x')
        self.assertEqual(1, len(extensions))
        self.assert_(42 in extensions)

        return

#### EOF ######################################################################