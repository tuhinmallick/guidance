from guidance import models, any_char

def test_single_char():
    model = models.Mock("<s>abc")
    assert str(f'{model}<s>{any_char()}') == "<s>a"