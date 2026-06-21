<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" />

  <xsl:template match="/classes">
    <xsl:text><!-- ubCode requirements: SPEC_DIS_TRANSLATION_LAYER, SPEC_MESSAGES_PAGE, REQ_DIS_INVESTIGATION_TOOLS -->
</xsl:text>

          <xsl:text>{% if pdu.pdu_name == '</xsl:text>
    <xsl:value-of select="class[initialValue/@name='pduType'][1]/@name" />
      <xsl:text>' %}&#10;    &lt;dl&gt;&#10;</xsl:text>
    <xsl:apply-templates select="class[initialValue/@name='pduType'][1]/attribute" mode="render-detail-fields" />
    <xsl:text>    &lt;/dl&gt;&#10;</xsl:text>

    <xsl:for-each select="class[initialValue/@name='pduType'][position() > 1]">
      <xsl:text>{% elif pdu.pdu_name == '</xsl:text>
        <xsl:value-of select="@name" />
      <xsl:text>' %}&#10;    &lt;dl&gt;&#10;</xsl:text>
      <xsl:apply-templates select="attribute" mode="render-detail-fields" />
      <xsl:text>    &lt;/dl&gt;&#10;</xsl:text>
      </xsl:for-each>
    <xsl:text>    {% else %}&#10;        {{ pdu.raw_payload|length }} bytes&#10;    {% endif %}</xsl:text>
  </xsl:template>

  <!-- Handle attribute flattening similar to django model generation -->
  <xsl:template match="attribute" mode="render-detail-fields">
    <xsl:variable name="refName" select="classRef/@name" />
    <xsl:variable name="attrName" select="@name" />
    <xsl:choose>
      <xsl:when test="$refName and //class[@name=$refName]">
    <xsl:text>        &lt;dt&gt;</xsl:text>
        <xsl:value-of select="$attrName" />
        <xsl:text>&lt;/dt&gt;&#10;        &lt;dd&gt;</xsl:text>
        <xsl:for-each select="//class[@name=$refName]/attribute">
          <xsl:text>{{ pdu.</xsl:text>
          <xsl:value-of select="concat($attrName, '_', @name)" />
          <xsl:text> }}</xsl:text>
          <xsl:if test="position() != last()">
            <xsl:text>, </xsl:text>
          </xsl:if>
        </xsl:for-each>
        <xsl:text>&lt;/dd&gt;&#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="render-detail-field">
          <xsl:with-param name="name" select="$attrName" />
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="render-detail-field">
    <xsl:param name="name" />
    <xsl:text>        &lt;dt&gt;</xsl:text>
    <xsl:value-of select="translate($name, ' ', '_')" />
    <xsl:text>&lt;/dt&gt;&#10;        &lt;dd&gt;{{ pdu.</xsl:text>
    <xsl:value-of select="translate($name, ' ', '_')" />
    <xsl:text> }}&lt;/dd&gt;&#10;</xsl:text>
  </xsl:template>
</xsl:stylesheet>

