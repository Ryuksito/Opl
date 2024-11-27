from src.models.nodes import *

import graphviz

class ASTVisualizer:
    def __init__(self, root_node):
        self.root = root_node
        self.dot = graphviz.Digraph(comment="Abstract Syntax Tree")
        self.idx = 0

    def visualize(self):
        self._add_nodes(self.root)
        self.dot.render("ast_visualization", view=True, format="png")

    def _add_nodes(self, node, parent=None, parent_label:str=None):
        if parent_label is None and parent is not None:
            raise Exception("Parent label")
        node_label = self._node_label(node, self.idx)
        self.idx += 1

        # Añade el nodo actual
        self.dot.node(node_label)

        if parent:
            # Crea una arista desde el nodo padre
            self.dot.edge(parent_label, node_label)

        print(type(node), node_label, parent_label)

        # Añade los hijos según el tipo de nodo
        if isinstance(node, BinOpNode):
            self._add_nodes(node.left_node, node, node_label)
            self._add_nodes(node.right_node, node, node_label)
        elif isinstance(node, UnaryOpNode):
            self._add_nodes(node.node, node, node_label)
        elif isinstance(node, ListNode):
            for element in node.element_nodes:
                self._add_nodes(element, node, node_label)
        elif isinstance(node, IfNode):
            for condition, expr, _ in node.cases:
                self._add_nodes(condition, node, node_label)
                self._add_nodes(expr, node, node_label)
            if node.else_case:
                self._add_nodes(node.else_case, node, node_label)
        elif isinstance(node, ForNode):
            self._add_nodes(node.start_value_node, node, node_label)
            self._add_nodes(node.end_value_node, node, node_label)
            if node.step_value_node:
                self._add_nodes(node.step_value_node, node, node_label)
            self._add_nodes(node.body_node, node, node_label)
        elif isinstance(node, WhileNode):
            self._add_nodes(node.condition_node, node, node_label)
            self._add_nodes(node.body_node, node, node_label)
        elif isinstance(node, FuncDefNode):
            self._add_nodes(node.body_node, node, node_label)
        elif isinstance(node, CallNode):
            self._add_nodes(node.node_to_call, node, node_label)
            for arg in node.arg_nodes:
                self._add_nodes(arg, node, node_label)
        elif isinstance(node, ReturnNode):
            if node.node_to_return:
                self._add_nodes(node.node_to_return, node, node_label)
        elif isinstance(node, VarAssignNode):
            self._add_nodes(node.value_node, node, node_label)
        elif isinstance(node, (NumberNode, StringNode, VarAccessNode)):
            # Los nodos hoja no tienen hijos
            pass

    def _node_label(self, node, differentiator:str=None):
        """
        Devuelve un identificador único y legible para un nodo.
        """
        if isinstance(node, NumberNode):
            return f"{differentiator}-Number({node.tok.value})"
        elif isinstance(node, StringNode):
            return f"{differentiator}-String({node.tok.value})"
        elif isinstance(node, VarAccessNode):
            return f"{differentiator}-Var({node.var_name_tok.value})"
        elif isinstance(node, VarAssignNode):
            return f"{differentiator}-Assign({node.var_name_tok.value})"
        elif isinstance(node, BinOpNode):
            return f"{differentiator}-BinOp({node.op_tok.value})"
        elif isinstance(node, UnaryOpNode):
            return f"{differentiator}-UnaryOp({node.op_tok.value})"
        elif isinstance(node, IfNode):
            return f"{differentiator}If"
        elif isinstance(node, ForNode):
            return f"{differentiator}For({node.var_name_tok.value})"
        elif isinstance(node, WhileNode):
            return f"{differentiator}While"
        elif isinstance(node, FuncDefNode):
            return f"{differentiator}Function({node.var_name_tok.value if node.var_name_tok else 'anonymous'})"
        elif isinstance(node, CallNode):
            return f"{differentiator}Call"
        elif isinstance(node, ReturnNode):
            return f"{differentiator}Return"
        elif isinstance(node, ListNode):
            return "Root"
        else:
            return f"{differentiator}{str(node).replace(':', '->')}"
