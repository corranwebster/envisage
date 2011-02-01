""" The default implementation of the 'IMessage' interface. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Str, implements

# Local imports.
from i_message import IMessage


class Message(HasTraits):
    """ The default implementation of the 'IMessage' interface. """

    implements(IMessage)

    # The author of the message.
    author = Str

    # The text of the message.
    text = Str

#### EOF ######################################################################