ladder_columns = {
    ('wins',0),
    ('losses',0),
    ('draws',0),
    ('prem_points',0),
    ('played',0),
    ('points_for',0),
    ('points_against',0),
    ('percentage',100),
    ('position',1)
}

ladder_cols = [i for i,j in ladder_columns]
h_ladder_form_cols = ['h_' + i + '_form' for i,j in ladder_columns]
a_ladder_form_cols = ['a_' + i + '_form' for i,j in ladder_columns]
h_ladder_form_cols_mapping = dict(zip(ladder_cols,h_ladder_form_cols))
a_ladder_form_cols_mapping = dict(zip(ladder_cols,a_ladder_form_cols))