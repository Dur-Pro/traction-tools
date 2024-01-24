/** @odoo-module **/

import KanbanRenderer from 'web.KanbanRenderer';
import KanbanView from 'web.KanbanView';
import KanbanRecord from 'web.KanbanRecord';
import viewRegistry from 'web.view_registry';
import core from 'web.core';

// Basically stolen from project module's project_kanban.js
const IssuesListKanbanRecord = KanbanRecord.extend({
    /**
     * @override
     * @private
     */
    _openRecord: function () {
        const kanbanBoxesElement = this.el.querySelectorAll('.o_issues_list_kanban_boxes a');
        if (this.selectionMode !== true && kanbanBoxesElement.length) {
            kanbanBoxesElement[0].click();
        } else {
            this._super.apply(this, arguments);
        }
    },
});

const IssuesListKanbanRenderer = KanbanRenderer.extend({
    config: _.extend({}, KanbanRenderer.prototype.config, {
        KanbanRecord: IssuesListKanbanRecord,
    }),
});

const IssuesListKanbanView = KanbanView.extend({
    config: Object.assign({}, KanbanView.prototype.config, {
        Renderer: IssuesListKanbanRenderer,
    })
});

viewRegistry.add('issues_list_kanban', IssuesListKanbanView);
