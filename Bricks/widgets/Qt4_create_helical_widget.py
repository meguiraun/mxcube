#
#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

import logging
import copy

from PyQt4 import QtCore
from PyQt4 import QtGui

import Qt4_queue_item
import Qt4_GraphicsManager as graphics_manager
import queue_model_objects_v1 as queue_model_objects

from queue_model_enumerables_v1 import EXPERIMENT_TYPE
from queue_model_enumerables_v1 import COLLECTION_ORIGIN
from Qt4_create_task_base import Qt4_CreateTaskBase
from Qt4_data_path_widget import Qt4_DataPathWidget
from Qt4_acquisition_widget import Qt4_AcquisitionWidget
from Qt4_processing_widget import Qt4_ProcessingWidget


class Qt4_CreateHelicalWidget(Qt4_CreateTaskBase):
    def __init__(self, parent = None,name = None, fl = 0):
        Qt4_CreateTaskBase.__init__(self, parent, name, fl, 'Helical')

        if not name:
            self.setName("create_helical_widget")

        """self.init_models()
        self._prev_pos = None
        self._current_pos = None
        self._list_item_map = {}
        self.init_models()

        v_layout = QtGui.QVBoxLayout(self, 2, 5, "v_layout")
        self._lines_gbox = QtGui.QGroupBox('Lines', self, "lines_gbox")
        self._lines_gbox.setColumnLayout(0, QtCore.Qt.Vertical)
        self._lines_gbox.layout().setSpacing(6)
        self._lines_gbox.layout().setMargin(11)
        lines_gbox_layout = QtGui.QHBoxLayout(self._lines_gbox.layout())
        lines_gbox_layout.setAlignment(QtCore.Qt.AlignTop)

        self._list_box = QtGui.QListBox(self._lines_gbox, "helical_page")
        self._list_box.setSelectionMode(qt.QListBox.Extended)
        self._list_box.setFixedWidth(175)
        self._list_box.setFixedHeight(50)
        list_box_tool_tip = "Select the line(s) to perfrom helical scan on"
        self._list_box.setToolTip(list_box_tool_tip)

        lines_gbox_layout.addWidget(self._list_box)

        button_layout = QtGui.QVBoxLayout(None, 0, 6, "button_layout")
        button_layout.setSpacing(5)
        add_button = QtGui.QPushButton("+", self._lines_gbox, "add_button")
        add_button.setFixedWidth(20)
        add_button.setFixedHeight(20)
        remove_button = QtGui.QPushButton("-", self._lines_gbox, "add_button")
        remove_button.setFixedWidth(20)
        remove_button.setFixedHeight(20)        
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        lines_gbox_layout.addLayout(button_layout)

        add_button_tool_tip = "Add a line between two saved positions, " \
                              "CTRL click to select more than one position"
        add_button.setToolTip(add_button_tool_tip)
        remove_button_tool_tip = "Remove selected line(s)"
        QtGui.QToolTip.add(remove_button, remove_button_tool_tip)

        self._acq_gbox = qt.QVGroupBox('Acquisition', self, 'acq_gbox')
        self._acq_widget = \
            Qt4_AcquisitionWidget(self._acq_gbox,
                              "acquisition_widget", layout='vertical',
                              acq_params=self._acquisition_parameters,
                              path_template=self._path_template)


        self._acq_widget.disable_inverse_beam(True)
        self._data_path_gbox = qt.QVGroupBox('Data location', self,
                                             'data_path_gbox')
        self._data_path_widget = \
            Qt4_DataPathWidget(self._data_path_gbox, 
                           data_model = self._path_template,
                           layout = 'vertical')

        self._processing_gbox = qt.QVGroupBox('Processing', self, 
                                              'processing_gbox')
        
        self._processing_widget = \
            Qt4_ProcessingWidget(self._processing_gbox,
                             data_model = self._processing_parameters)

        v_layout.addWidget(self._lines_gbox)
        v_layout.addWidget(self._acq_gbox)
        v_layout.addWidget(self._data_path_gbox)
        v_layout.addWidget(self._processing_gbox)

        qt.QObject.connect(add_button, qt.SIGNAL("clicked()"),
                        self.add_clicked)

        qt.QObject.connect(remove_button, qt.SIGNAL("clicked()"),
                        self.remove_clicked)

        qt.QObject.connect(self._list_box, qt.SIGNAL("selectionChanged()"),
                           self.list_box_selection_changed)

        prefix_ledit = self._data_path_widget.\
                       data_path_widget_layout.child('prefix_ledit')

        run_number_ledit = self._data_path_widget.\
                           data_path_widget_layout.child('run_number_ledit')

        self.connect(prefix_ledit, 
                     qt.SIGNAL("textChanged(const QString &)"), 
                     self._prefix_ledit_change)

        self.connect(run_number_ledit,
                     qt.SIGNAL("textChanged(const QString &)"), 
                     self._run_number_ledit_change)

        self.connect(self._data_path_widget,
                     qt.PYSIGNAL("path_template_changed"),
                     self.handle_path_conflict)"""

    def init_models(self):
        Qt4_CreateTaskBase.init_models(self)
        self._energy_scan_result = queue_model_objects.EnergyScanResult()
        self._processing_parameters = queue_model_objects.ProcessingParameters()
  
        """if self._beamline_setup_hwobj is not None:
            has_shutter_less = self._beamline_setup_hwobj.\
                               detector_has_shutterless()
            self._acquisition_parameters.shutterless = has_shutter_less

            self._acquisition_parameters = self._beamline_setup_hwobj.\
                get_default_acquisition_parameters()
        else:
            self._acquisition_parameters = queue_model_objects.AcquisitionParameters()
            self._path_template = queue_model_objects.PathTemplate()"""

    def add_clicked(self):
        selected_shapes = self._graphics_manager.selected_shapes.values()

        if len(selected_shapes) == 2:
            p1 = selected_shapes[1]
            p2 = selected_shapes[0]
            
            line = graphics_manager.\
                   Line(self._graphics_manager.get_drawing(),
                        p1.qub_point, p2.qub_point,
                        p1.centred_position, p2.centred_position)

            line.show()
            self._graphics_manager.add_shape(line)
            list_box_item = qt.QListBoxText(self._list_box, 'Line')
            self._list_item_map[list_box_item] = line

            # De select previous items
            for item in self.selected_items():
                self._list_box.setSelected(item, False)
            
            self._list_box.setSelected(list_box_item, True)

    def remove_clicked(self):
        selected_items = self.selected_items()

        if selected_items:
            for item in selected_items:
                self._list_box.removeItem(self._list_box.index(item))
                line = self._list_item_map[item]
                self._graphics_manager.delete_shape(line)
                del self._list_item_map[item]

    # Calback from graphics_manager, called when a shape is deleted
    def shape_deleted(self, shape):
        if isinstance(shape, graphics_manager.Point):
            items_to_remove = []

            for (list_item, line) in self._list_item_map.iteritems():
                for qub_object in shape.get_qub_objects():
                    if qub_object in line.get_qub_objects():
                        items_to_remove.append((list_item, line))

            for (list_item, line) in items_to_remove:
                self._list_box.removeItem(self._list_box.index(list_item))
                del self._list_item_map[list_item]

    def centred_position_selection(self, positions):
        if len(positions) == 1:
            self._prev_pos = positions[0]
            
        elif len(positions) == 2:

            for pos in positions:
                if pos != self._prev_pos:
                    self._current_pos = pos
        else:
            self._prev_pos = None
            self._current_pos = None

    def list_box_selection_changed(self):
        self.show_selected_lines()

    def selected_items(self):
        selected_items = []
                
        for item_index in range(0, self._list_box.numRows()):
            if self._list_box.isSelected(item_index):
                selected_items.append(self._list_box.item(item_index))

        return selected_items
        
    def show_selected_lines(self):
        selected_items = self.selected_items()

        for list_item in self._list_item_map.keys():
            line = self._list_item_map[list_item]
            if list_item in selected_items:
                self._graphics_manager.select_shape(line)
            else:
                self._graphics_manager.de_select_shape(line)

    def approve_creation(self):
        base_result = Qt4_CreateTaskBase.approve_creation(self)
    
        selected_lines = False
        
        if self.selected_items():
            selected_lines = True
        else:
            logging.getLogger("user_level_log").\
                warning("No lines selected, please select one or more lines.")

        return base_result and selected_lines 
            
    def update_processing_parameters(self, crystal):
        self._processing_parameters.space_group = crystal.space_group
        self._processing_parameters.cell_a = crystal.cell_a
        self._processing_parameters.cell_alpha = crystal.cell_alpha
        self._processing_parameters.cell_b = crystal.cell_b
        self._processing_parameters.cell_beta = crystal.cell_beta
        self._processing_parameters.cell_c = crystal.cell_c
        self._processing_parameters.cell_gamma = crystal.cell_gamma
        self._processing_widget.update_data_model(self._processing_parameters)

    def select_shape_with_cpos(self, start_cpos, end_cpos):
        self._graphics_manager.de_select_all()
        selected_line = None

        for shape in self._graphics_manager.get_shapes():
            if isinstance(shape, graphics_manager.Line):
                if shape.get_centred_positions()[0] == start_cpos and\
                       shape.get_centred_positions()[1] == end_cpos:
                    self._graphics_manager.select_shape(shape)
                    selected_line = shape

        #de-select previous selected list items and
        #select the current shape (Line).
        for (list_item, shape) in self._list_item_map.iteritems():

            if selected_line is shape:
                self._list_box.setSelected(list_item, True)
            else:
                self._list_box.setSelected(list_item, False)

    def single_item_selection(self, tree_item):
        Qt4_CreateTaskBase.single_item_selection(self, tree_item)
                                                             
        if isinstance(tree_item, Qt4_queue_item.SampleQueueItem):
            sample_model = tree_item.get_model()
            self._processing_parameters = sample_model.processing_parameters
            #self._processing_parameters = copy.deepcopy(self._processing_parameters)
            self._processing_widget.update_data_model(self._processing_parameters)

        elif isinstance(tree_item, Qt4_queue_item.DataCollectionQueueItem):
            data_collection = tree_item.get_model()

            if data_collection.experiment_type == EXPERIMENT_TYPE.HELICAL:
                if tree_item.get_model().is_executed():
                    self.setDisabled(True)
                else:
                    self.setDisabled(False)

                self._path_template = data_collection.get_path_template()
                self._data_path_widget.update_data_model(self._path_template)
                
                self._acquisition_parameters = data_collection.acquisitions[0].\
                                               acquisition_parameters

                if len(data_collection.acquisitions) == 2:
                    start_cpos = data_collection.acquisitions[0].acquisition_parameters.\
                                 centred_position
                    end_cpos = data_collection.acquisitions[1].acquisition_parameters.\
                               centred_position

                    self.select_shape_with_cpos(start_cpos, end_cpos)

                self._acq_widget.update_data_model(self._acquisition_parameters,
                                                   self._path_template)
                self.get_acquisition_widget().use_osc_start(True)
                
                self._processing_parameters = data_collection.processing_parameters
                self._processing_widget.update_data_model(self._processing_parameters)
            else:
                self.setDisabled(True)
        else:
            self.setDisabled(True)

        if isinstance(tree_item, Qt4_queue_item.SampleQueueItem) or \
           isinstance(tree_item, Qt4_queue_item.DataCollectionGroupQueueItem) or \
           isinstance(tree_item, Qt4_queue_item.DataCollectionQueueItem):

            self._processing_widget.update_data_model(self._processing_parameters)
            self._acq_widget.update_data_model(self._acquisition_parameters,
                                               self._path_template)
  
    def _create_task(self,  sample, shape):
        data_collections = []

        if isinstance(shape, graphics_manager.Line ):
            if shape.get_qub_objects() is not None:
                snapshot = self._graphics_manager.get_snapshot(shape.get_qub_objects())
            else:
                snapshot = self._graphics_manager.get_snapshot([])

            # Acquisition for start position
            start_acq = self._create_acq(sample) 
            
            start_acq.acquisition_parameters.\
                centred_position = copy.deepcopy(shape.start_cpos)
            start_acq.acquisition_parameters.centred_position.\
                snapshot_image = snapshot

            start_acq.path_template.suffix = self._session_hwobj.suffix

            # Add another acquisition for the end position
            end_acq = self._create_acq(sample)

            end_acq.acquisition_parameters.\
                centred_position = shape.end_cpos
            end_acq.acquisition_parameters.centred_position.\
                snapshot_image = snapshot

            end_acq.path_template.suffix = self._session_hwobj.suffix

            processing_parameters = copy.deepcopy(self._processing_parameters)

            dc = queue_model_objects.DataCollection([start_acq, end_acq],
                                    sample.crystals[0],
                                    processing_parameters)

            dc.set_name(start_acq.path_template.get_prefix())
            dc.set_number(start_acq.path_template.run_number)
            dc.experiment_type = EXPERIMENT_TYPE.HELICAL

            data_collections.append(dc)
            self._path_template.run_number += 1

        return data_collections
                   