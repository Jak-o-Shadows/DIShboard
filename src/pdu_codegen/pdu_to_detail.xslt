<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" />

  <xsl:template match="/classes">
    <xsl:text><!-- ubCode requirements: SPEC_DIS_TRANSLATION_LAYER, SPEC_MESSAGES_PAGE, REQ_DIS_INVESTIGATION_TOOLS -->
</xsl:text>
    <xsl:text>{% if pdu.pdu_name == 'EntityStatePdu' %}</xsl:text>
    <xsl:text>&#10;    &lt;div class="grid"&gt;&#10;        &lt;div&gt;Entity: {{ pdu.entityID_siteID }}:{{ pdu.entityID_applicationID }}:{{ pdu.entityID_entityID }}&lt;/div&gt;&#10;        &lt;div&gt;Loc: {{ pdu.entityLocation_x|floatformat:1 }}, {{ pdu.entityLocation_y|floatformat:1 }}&lt;/div&gt;&#10;    &lt;/div&gt;&#10;</xsl:text>

    <xsl:for-each select="class[initialValue/@name='pduType']">
      <xsl:text>    {% elif pdu.pdu_name == '</xsl:text>
      <xsl:value-of select="@name" />
      <xsl:text>' %}&#10;    &lt;div class="grid"&gt;&#10;</xsl:text>

      <xsl:for-each select="attribute">
        <xsl:text>        &lt;div&gt;</xsl:text>
        <xsl:value-of select="@name" />
        <xsl:text>: {{ pdu.</xsl:text>
        <xsl:value-of select="@name" />
        <xsl:text> }}&lt;/div&gt;&#10;</xsl:text>
      </xsl:for-each>

      <xsl:text>    &lt;/div&gt;&#10;</xsl:text>
    </xsl:for-each>

    <xsl:text>    {% else %}&#10;        {{ pdu.raw_payload|length }} bytes&#10;    {% endif %}</xsl:text>
  </xsl:template>
</xsl:stylesheet>

