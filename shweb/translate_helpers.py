from flask_babel import _


def get_release_types():
    return {
        'Single': _('Single'),
        'Album': _('Album'),
        'Ep': _('Ep'),
        'single': _('single'),
        'album': _('album'),
        'ep': _('ep')
    }


def get_month_names():
    return [
        _('jan'),
        _('feb'),
        _('mar'),
        _('apr'),
        _('may'),
        _('jun'),
        _('jul'),
        _('aug'),
        _('sep'),
        _('oct'),
        _('nov'),
        _('dec')
    ]
