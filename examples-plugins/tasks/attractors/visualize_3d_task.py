# Enthought library imports.
from enthought.pyface.tasks.action.api import SGroup, SMenu, SMenuBar, \
    TaskToggleGroup
from enthought.pyface.tasks.api import Task, TaskLayout
from enthought.traits.api import Any, List

# Local imports.
from model_config_pane import ModelConfigPane
from model_help_pane import ModelHelpPane
from plot_3d_pane import Plot3dPane


class Visualize3dTask(Task):
    """ A task for visualizing attractors in 3D.
    """

    #### 'Task' interface #####################################################

    id = 'example.attractors.task_3d'
    name = '3D Visualization'

    menu_bar = SMenuBar(SMenu(id='File', name='&File'),
                        SMenu(id='Edit', name='&Edit'),
                        SMenu(TaskToggleGroup(),
                              id='View', name='&View'))

    #### 'Visualize3dTask' interface ##########################################

    # The attractor model that is currently active (visible in the center pane).
    active_model = Any

    # The list of available attractor models.
    models = List

    ###########################################################################
    # 'Task' interface.
    ###########################################################################

    def create_central_pane(self):
        """ Create a plot pane with a list of models. Keep track of which model
            is active so that dock panes can introspect it.
        """
        pane = Plot3dPane(models=self.models)

        self.active_model = pane.active_model
        pane.on_trait_change(self._update_active_model, 'active_model')

        return pane

    def create_dock_panes(self):
        return [ ModelConfigPane(model=self.active_model),
                 ModelHelpPane(model=self.active_model) ]

    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _default_layout_default(self):
        return TaskLayout(left_panes=[['example.attractors.model_config_pane',
                                       'example.attractors.model_help_pane']])

    def _models_default(self):
        from model.lorenz import Lorenz
        from model.rossler import Rossler
        return [ Lorenz(), Rossler() ]

    #### Trait change handlers ################################################

    def _update_active_model(self):
        self.active_model = self.window.central_pane.active_model
        for dock_pane in self.window.dock_panes:
            dock_pane.model = self.active_model