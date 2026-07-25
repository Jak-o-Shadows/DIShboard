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

class PduFilterForm(forms.Form):
    # @PDU Type Filter, SPEC_FILTER_PROTOCOL, code_impl, SPEC_FILTER_PROTOCOL
    pdu_type = forms.MultipleChoiceField(
        label='PDU Type',
        required=False,
    )

    # @Time Range Filter, SPEC_FILTER_TEMPORAL, code_impl, SPEC_FILTER_TEMPORAL
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)

    # @Tactical Filter, SPEC_FILTER_TACTICAL, code_impl, SPEC_FILTER_TACTICAL
    force_id = forms.ChoiceField(required=False)
    site_id = forms.IntegerField(required=False)
    application_id = forms.IntegerField(required=False)
    exercise_id = forms.IntegerField(required=False)

    # @Entity Filter, SPEC_FILTER_ENTITY, code_impl, SPEC_FILTER_ENTITY
    entity_id = forms.IntegerField(required=False)
    entity_kind = forms.ChoiceField(required=False)
    entity_domain = forms.ChoiceField(required=False)
    entity_category = forms.ChoiceField(required=False)

    # @Diagnostic Filter, SPEC_FILTER_DIAGNOSTIC, code_impl, SPEC_FILTER_DIAGNOSTIC
    raw_sql = forms.CharField(required=False)
    show_malformed = forms.BooleanField(required=False)
