<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" />
  
  <xsl:template match="/classes">
    <xsl:text># ubCode requirements: SPEC_DIS_TRANSLATION_LAYER, SPEC_MESSAGES_PAGE, REQ_DIS_INVESTIGATION_TOOLS
# Generated from DIS PDU spec to support code-linked requirement traceability
from django.db import models

</xsl:text>
    <xsl:for-each select="class[initialValue/@name='pduType']">
      <xsl:text>class </xsl:text>
      <xsl:value-of select="@name" />
      <xsl:text>(models.Model):
</xsl:text>
      <xsl:apply-templates select="attribute" />
        <xsl:text>
    @property
    def pdu_name(self):
        return self.__class__.__name__

</xsl:text>
      </xsl:for-each>
  </xsl:template>

  <!-- Template to process attributes and flatten referenced classes -->
  <xsl:template match="attribute">
    <xsl:variable name="refName" select="classRef/@name" />
    <xsl:variable name="attrName" select="@name" />
    <xsl:choose>
      <!-- Flatten referenced classes -->
      <xsl:when test="$refName and //class[@name=$refName]">
        <xsl:for-each select="//class[@name=$refName]/attribute">
          <xsl:call-template name="render-field">
            <xsl:with-param name="name" select="concat($attrName, '_', @name)" />
          </xsl:call-template>
        </xsl:for-each>
      </xsl:when>
      <!-- Render regular primitive field -->
      <xsl:otherwise>
        <xsl:call-template name="render-field">
          <xsl:with-param name="name" select="$attrName" />
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="render-field">
    <xsl:param name="name" />
    <xsl:text>    </xsl:text>
    <xsl:value-of select="translate($name, ' ', '_')" />
    <xsl:text> = </xsl:text>
    <xsl:choose>
      <xsl:when test="primitive[@type='unsigned short' or @type='unsigned int' or @type='unsigned byte' or @type='short' or @type='byte' or @type='int' or @type='long']">
        <xsl:text>models.IntegerField()</xsl:text>
      </xsl:when>
      <xsl:when test="primitive[@type='float' or @type='double']">
        <xsl:text>models.FloatField()</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>models.CharField(max_length=255)</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>
</xsl:text>
  </xsl:template>
</xsl:stylesheet>

