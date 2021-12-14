class TokenPatern:
    def __init__(self, type, regexp):
        self.type = type
        self.regexp = regexp
       

TokenPaterns = {
    'CREATETABLE':TokenPatern('CREATETABLE', 'CREATETABLE'),
    'INDEXED':TokenPatern('INDEXED','INDEXED'),
    'COMMA':TokenPatern('COMMA', ','),
    '(':TokenPatern('(','\\('),
    ')':TokenPatern(')','\\)'),
    '[':TokenPatern('[','\\['),
    ']':TokenPatern(']','\\]'),
    'VAR':TokenPatern('VAR','[_a-z][_a-z0-9]+'),
    'NUMBER': TokenPatern('NUMBER','[-+]?[0-9]+' ),
    'SELECT':TokenPatern('SELECT','SELECT'),
    'FROM':TokenPatern('FROM','FROM'),
    'INSERTINTO':TokenPatern('INSERTINTO', 'INSERTINTO'),
    'WHERE':TokenPatern('WHERE','WHERE'),
    'GROUPBY':TokenPatern('GROUPBY','GROUPBY'),
    'DELETE':TokenPatern('DELETE','DELETE'),
    'EQUAL': TokenPatern('EQUAL','='),
    'NOT_EQUAL':TokenPatern('NOT_EQUAL','!='),
    'MORE_EQUAL':TokenPatern('MORE_EQUAL','>='),
    'LESS_EQUAL': TokenPatern('LESS_EQUAL','<='),
    'LESS':TokenPatern('LESS','<'),
    'MORE':TokenPatern('MORE','>'),
    'ALL':TokenPatern('ALL','\\*'),
    'COUNT':TokenPatern('COUNT','COUNT$'),
    'COUNT_DISTINCT':TokenPatern('COUNT_DISTINCT','COUNT_DISTINCT'),
    'MAX':TokenPatern('MAX','MAX'),
    'AVG':TokenPatern('AVG','AVG'),
    'SEMICOLON':TokenPatern('SEMICOLON', ';')
}