from collections import OrderedDict
from typing import Self

__all__ = [
    'MenuItem',
    'menubar_description',
    'menu_actions',
]


class MenuItem:
    """Элемент меню"""

    def __init__(self, label: str, code: str, children: list[Self] | None = None):
        self.label = label
        self.code = code
        self.parent: Self | None = None
        self.children: list[Self] = children if children is not None else []
        self._set_children_parent()

    def __str__(self):
        return self.full_path

    def _set_children_parent(self):
        """Установка дочерним элементам родительского"""
        for c in self.children:
            c.parent = self

    @property
    def full_code(self) -> str:
        if self.parent:
            return f'{self.parent.full_code}.{self.code}'
        return self.code

    @property
    def full_path(self) -> str:
        if self.parent:
            return f'{self.parent.full_path}->{self.label}'
        return self.label

    @property
    def is_action(self) -> bool:
        return not self.children


menubar_description: OrderedDict[str, MenuItem] = OrderedDict()
menubar_description['file'] = MenuItem(
    label='File',
    code='file',
    children=[
        MenuItem(
            label='Open',
            code='open',
        ),
        MenuItem(
            label='Save',
            code='save',
        ),
        MenuItem(
            label='New',
            code='new',
        ),
        MenuItem(
            label='Close',
            code='close',
        ),
        MenuItem(
            label='Export',
            code='export',
            children=[
                MenuItem(
                    label='XLSX',
                    code='xlsx',
                ),
                MenuItem(
                    label='XLS',
                    code='xls',
                ),
                MenuItem(
                    label='CSV',
                    code='csv',
                    children=[
                        MenuItem(
                            label='separator ;',
                            code='separator_semicolon',
                        ),
                        MenuItem(
                            label='separator ,',
                            code='separator_comma',
                        )
                    ],
                )
            ],
        )
    ],
)
menubar_description['edit'] = MenuItem(
    label='Edit',
    code='edit',
    children=[
        MenuItem(
            label='Cut',
            code='cut',
        ),
        MenuItem(
            label='Copy',
            code='copy',
        ),
        MenuItem(
            label='Paste',
            code='paste',
        ),
        MenuItem(
            label='Delete',
            code='delete',
        )
    ],
)
menubar_description['view'] = MenuItem(
    label='View',
    code='view',
    children=[
        MenuItem(
            label='Ruler',
            code='ruler',
        ),
        MenuItem(
            label='Grid',
            code='grid',
        ),
        MenuItem(
            label='Tools',
            code='tools',
            children=[],
        ),
        MenuItem(
            label='Font',
            code='font',
            children=[
                MenuItem(
                    label='Size',
                    code='size',
                    children=[
                        MenuItem(
                            label='Increase',
                            code='increase_font',
                        ),
                        MenuItem(
                            label='Decrease',
                            code='decrease_font',
                        )
                    ]
                )
            ]
        ),
        MenuItem(
            label='Color',
            code='color',
        ),
        MenuItem(
            label='Scale',
            code='scale',
            children=[
                MenuItem(
                    label='Increase',
                    code='increase_scale',
                ),
                MenuItem(
                    label='Decrease',
                    code='decrease_scale',
                )
            ]
        )
    ],
)
menubar_description['window'] = MenuItem(
    label='Window',
    code='window',
    children=[],
)
menubar_description['help'] = MenuItem(
    label='Help',
    code='help',
    children=[
        MenuItem(
            label='Registration',
            code='registration',
        ),
        MenuItem(
            label='About',
            code='about',
        ),
        MenuItem(
            label='Payment',
            code='payment',
        )
    ],
)

menu_actions: list[MenuItem] = []


def _collect_menu_actions() -> None:
    queue = list(menubar_description.values())
    while True:
        if not queue:
            break
        item = queue.pop(0)
        if item.is_action:
            menu_actions.append(item)
        else:
            queue.extend(item.children)


_collect_menu_actions()
