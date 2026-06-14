from django import forms


class PlaybackSenderForm(forms.Form):
    duration_seconds = forms.IntegerField(
        label='Duration (seconds)',
        min_value=1,
        initial=30,
        help_text='How long to send synthetic PDUs.',
    )
    destination_host = forms.GenericIPAddressField(
        label='Destination IP',
        initial='127.0.0.1',
        protocol='both',
        unpack_ipv4=False,
        help_text='Target address for the synthetic DIS traffic.',
    )
    destination_port = forms.IntegerField(
        label='Destination port',
        min_value=1,
        max_value=65535,
        initial=3500,
        help_text='Target UDP port for the synthetic DIS traffic.',
    )


class ConnectionSettingsForm(forms.Form):
    listen_host = forms.GenericIPAddressField(
        label='Listen Host',
        initial='0.0.0.0',
        protocol='both',
        unpack_ipv4=False,
        help_text='Local address to bind for DIS ingestion.',
    )
    listen_port = forms.IntegerField(
        label='Listen Port',
        min_value=1,
        max_value=65535,
        initial=3500,
        help_text='UDP port to receive DIS packets on.',
    )
