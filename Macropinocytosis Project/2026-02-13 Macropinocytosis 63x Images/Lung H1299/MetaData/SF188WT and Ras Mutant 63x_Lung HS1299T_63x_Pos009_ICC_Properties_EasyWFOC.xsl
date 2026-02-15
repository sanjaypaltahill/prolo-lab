<?xml version="1.0"?><!-- Created with Liquid XML Studio Starter Edition 9.1.11.3570 (http://www.liquid-technologies.com) --><!DOCTYPE xsl:stylesheet[
  <!ENTITY nbsp "&#160;">
]><xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dt="urn:schemas-microsoft-com:datatypes"><xsl:output method="html" /><xsl:param name="tempVal" select="none" /><xsl:variable name="NormalFontStyle">font-family: Segoe UI; font-size: 10pt; font-weight: normal</xsl:variable><xsl:variable name="BoldFontStyle">font-family: Segoe UI; font-size: 10pt; font-weight: bold</xsl:variable><xsl:template match="/"><HTML><HEAD><TITLE><xsl:value-of select="@Name" /></TITLE><script type="text/javascript">
          var timestampVisible = 0;
          function Show()
          {
          if(timestampVisible == 0)
          {
          window.document.getElementById("ID_1").style.display = "none";
          window.document.getElementById("ID_2").style.display = "block";
          timestampVisible = 1;
          }
          else
          {
          window.document.getElementById("ID_1").style.display = "block";
          window.document.getElementById("ID_2").style.display = "none";
          timestampVisible = 0;
          }
          }
        </script></HEAD><BODY topmargin="0px" leftmargin="0px" bgcolor="#2B2B2B"><xsl:apply-templates select="Data" /></BODY></HTML></xsl:template><xsl:template match="HumanReadableInformation"><xsl:apply-templates select="InfoCategoryList" /></xsl:template><xsl:template match="InfoCategoryList"><hr /><!-- irgendwas außen herum ?? --><xsl:apply-templates select="InfoCategory" /><!-- irgendwas außen herum ?? --></xsl:template><xsl:template match="InfoCategory"><!-- <HR width="98%" /> --><TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="15"><TR><TD align="left" style="{$NormalFontStyle}; color: #FFFFFF; padding: 1px;"><u><b><xsl:value-of select="Caption" /></b></u></TD></TR><xsl:for-each select="Line"><xsl:variable name="Indentation"><xsl:if test="starts-with(.,'  ')">&nbsp;&nbsp;&nbsp;</xsl:if></xsl:variable><TR><xsl:choose><xsl:when test="@Format = 'bad'"><TD align="left" style="{$NormalFontStyle}; color: E11A1A; padding: 1px;"><xsl:value-of select="$Indentation" /><xsl:value-of select="." /></TD></xsl:when><xsl:when test="@Format = 'good'"><TD align="left" style="{$NormalFontStyle}; color: 00FF00; padding: 1px;"><xsl:value-of select="$Indentation" /><xsl:value-of select="." /></TD></xsl:when><xsl:otherwise><TD align="left" style="{$NormalFontStyle}; color: FFFFFF; padding: 1px;"><xsl:value-of select="$Indentation" /><xsl:value-of select="." /></TD></xsl:otherwise></xsl:choose></TR></xsl:for-each></TABLE><br /></xsl:template><xsl:template match="Data"><xsl:apply-templates select="Image/ImageDescription" /><xsl:apply-templates select="User-Comment" /><xsl:apply-templates select="HumanReadableInformation" /><xsl:apply-templates select="Image/TimeStampList" /></xsl:template><xsl:template match="User-Comment"></xsl:template><xsl:template name="break"><xsl:param name="text" select="//User-Comment" /><xsl:comment>This inserts line breaks into the user description in place of line feeds</xsl:comment><xsl:choose><xsl:when test="contains($text, '&#xA;')"><xsl:value-of select="substring-before($text, '&#xA;')" /><br /><xsl:call-template name="break"><xsl:with-param name="text" select="substring-after($text,'&#xA;')" /></xsl:call-template></xsl:when><xsl:otherwise><xsl:value-of select="$text" /></xsl:otherwise></xsl:choose></xsl:template><xsl:template match="ImageDescription"><xsl:variable name="isFileSaved"><xsl:if test="FileLocation != ' '">1</xsl:if></xsl:variable><TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#2B2B2B"><TR><TD><TABLE width="100%" align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#2B2B2B"><TR><TD align="center" valign="center" bgcolor="#2B2B2B"><xsl:choose><xsl:when test="0 != string-length(@ThumbnailPNGImage)"><img style="align:center; valign:middle" border="0" alt="thumbnail" src="data:image/png;base64,{@ThumbnailPNGImage}" /></xsl:when><xsl:otherwise></xsl:otherwise></xsl:choose></TD><TD><TABLE width="100%" align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#2B2B2B"><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD height="20" width="35%">Image: </TD><TD><B><xsl:value-of select="Name" /></B></TD></TR><xsl:choose><xsl:when test="//Data/Image/Attachment[@Name='HardwareSetting']/LDM_Block_Widefield_Sequential/LDM_Block_Sequential_Master/ATLCameraSettingDefinition/@UserManagementUserName != 'UserManagementFeatureInactive'"><xsl:variable name="UserManagementUserName"><xsl:value-of select="//Data/Image/Attachment[@Name='HardwareSetting']/LDM_Block_Widefield_Sequential/LDM_Block_Sequential_Master/ATLCameraSettingDefinition/@UserManagementUserName" /></xsl:variable><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD width="40%">
                          User :
                        </TD><TD><xsl:value-of select="$UserManagementUserName" /></TD></TR></xsl:when></xsl:choose><xsl:if test="$isFileSaved = '1'"><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD width="35%">File Location: </TD><TD><xsl:value-of select="FileLocation" /></TD></TR></xsl:if><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD width="35%">Size: </TD><TD><xsl:value-of select="Size" /></TD></TR><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD width="35%">Start Time: </TD><TD><xsl:value-of select="StartTime" /></TD></TR><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD width="35%">End Time: </TD><TD><xsl:value-of select="EndTime" /></TD></TR><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD width="35%">Total Exposures: </TD><TD><xsl:value-of select="FrameCount" /></TD></TR></TABLE></TD><TD align="center" valign="top" rowspan="2"><A href="http://www.confocal-microscopy.com/" target="about:blank"><IMG src="LeicaLogo_Transparent_WhiteText.png" padding="20" border="0" alt="Leica Microsystems CMS GmbH" /></A></TD></TR></TABLE></TD></TR></TABLE><xsl:if test="//User-Comment != ' '"><hr /><TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="5" bgcolor="#2B2B2B"><TR><TD><TABLE topmargin="0" leftmargin="0" width="100%" align="center" border="0" cellspacing="0" cellpadding="5" bgcolor="#2B2B2B"><TR style="{$NormalFontStyle}; color: #FFFFFF; padding: 3px;"><TD colspan="2" width="35%"><xsl:call-template name="break" /></TD></TR></TABLE></TD></TR></TABLE></xsl:if><!--
        <BR />
        <xsl:variable name="isImageAlignmentEnabled">
            <xsl:comment>Variable for display Multi-Camera settings</xsl:comment>
            <xsl:if test="//ATLCameraSettingDefinition/@IsImageAlignmentEnabled = '1'">1</xsl:if>
        </xsl:variable>
        <BR />
        <xsl:if test="$isImageAlignmentEnabled = '1'">
            <BR />
            <HR width="98%" />
            <TABLE width="98%" align="center" border="0" cellspacing="5" cellpadding="5">
                <TR>
                    <TD align="left" style="{$NormalFontStyle}; padding: 3px;">
                        <b>Image Alignment settings</b>
                    </TD>
                </TR>
            </TABLE>
            <xsl:for-each select="//ATLCameraSettingDefinition/ImageAlignmentSettings/MultiCamImageAlignment">
                <TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="5" bgcolor="#DDDAD7">
                    <TR style="font-family: Segoe UI; font-size: 10pt; font-weight: normal; padding: 3px;">
                        <TD colspan="2">
                            <TABLE topmargin="0" leftmargin="0" width="100%" align="center" border="1" cellspacing="0" cellpadding="0" bgcolor="#FFFFFF">
                                <TR style="{$NormalFontStyle}; color: 000000; padding: 3px;">
                                    <TD width="40%">
                                        Settings between
                                    </TD>
                                    <TD>
                                        <xsl:value-of select="@CameraNameBase" /> and
                                        <xsl:value-of select="@CameraNameCurrent" />
                                    </TD>
                                </TR>
                                <TR style="{$NormalFontStyle}; color: 000000; padding: 3px;">
                                    <TD width="40%">
                                        Multi Camera Rotation angle
                                    </TD>
                                    <TD>
                                        <xsl:value-of select="@RotationAngle" />&nbsp; deg
                                    </TD>
                                </TR>
                                <TR style="{$NormalFontStyle}; color: 000000; padding: 3px;">
                                    <TD width="40%">
                                        Multi Camera Offset X
                                    </TD>
                                    <TD>
                                        <xsl:value-of select="@TranslationX" />&nbsp; px
                                    </TD>
                                </TR>
                                <TR style="{$NormalFontStyle}; color: 000000; padding: 3px;">
                                    <TD width="40%">
                                        Multi Camera Offset Y
                                    </TD>
                                    <TD>
                                        <xsl:value-of select="@TranslationY" />&nbsp; px
                                    </TD>
                                </TR>
                                <TR style="{$NormalFontStyle}; color: 000000; padding: 3px;">
                                    <TD width="40%">
                                        Multi Camera Scale
                                    </TD>
                                    <TD>
                                        <xsl:value-of select="format-number(@Scale,'#%')" />
                                    </TD>
                                </TR>
                            </TABLE>
                        </TD>
                    </TR>
                </TABLE>
            </xsl:for-each>
        </xsl:if>
--></xsl:template><xsl:template match="TimeStampList"><br /><TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="5"><TR><TD align="left" style="{$NormalFontStyle}; color: #FFFFFF; padding: 1px;"><b><u>Time Stamps</u></b>&nbsp;</TD></TR></TABLE><DIV ID="ID_1" style="display:block;"><TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#2B2B2B"><TR><TD><TABLE topmargin="0" leftmargin="0" width="100%" align="left" border="1" cellspacing="0" cellpadding="3" bgcolor="#2B2B2B"><TR style="{$BoldFontStyle}; color: #FFFFFF; padding: 3px;"><TD>
                  Frame &nbsp; (<a href="javascript:Show()">Show All</a>)
                </TD><TD>Relative Time (s)</TD><TD>Absolute Time (h:m:s.ms)</TD><TD>Date</TD></TR><xsl:for-each select="TimeStamp"><xsl:if test="not(position()!=1 and position()!=last())"><TR style="font-family: Segoe UI; font-size: 9pt; font-weight: normal; color: #FFFFFF; padding: 3px;"><TD><xsl:number value="position()" format="1 " /></TD><TD><xsl:choose><xsl:when test="@RelativeTime != ''"><xsl:value-of select="@RelativeTime" /></xsl:when><xsl:otherwise> --- </xsl:otherwise></xsl:choose></TD><TD><xsl:value-of select="@Time" />.<xsl:value-of select="@MiliSeconds" /></TD><TD><xsl:choose><xsl:when test="@Date != ''"><xsl:value-of select="@Date" /></xsl:when><xsl:otherwise> --- </xsl:otherwise></xsl:choose></TD></TR></xsl:if></xsl:for-each></TABLE></TD></TR></TABLE><BR /></DIV><DIV ID="ID_2" style="display:none;"><TABLE width="98%" align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#2B2B2B"><TR><TD><TABLE topmargin="0" leftmargin="0" width="100%" align="left" border="1" cellspacing="0" cellpadding="5" bgcolor="#2B2B2B"><TR style="{$BoldFontStyle}; color: #FFFFFF; padding: 3px;"><TD>
                  Frame &nbsp; (<a href="javascript:Show()">Show first + last</a>)
                </TD><TD>Relative Time</TD><TD>Absolute Time</TD><TD>Date</TD></TR><xsl:for-each select="TimeStamp"><TR style="font-family: Segoe UI; font-size: 9pt; font-weight: normal; color: #FFFFFF; padding: 3px;"><TD><xsl:number value="position()" format="1 " /></TD><TD><xsl:value-of select="@RelativeTime" /></TD><TD><xsl:value-of select="@Time" />.<xsl:value-of select="@MiliSeconds" /></TD><TD><xsl:value-of select="@Date" /></TD></TR></xsl:for-each></TABLE></TD></TR></TABLE></DIV><BR /></xsl:template><xsl:template match="Attachment[@Name='Annotation']" /><xsl:template match="Attachment[@Name='DeconvolutionExpertSettings']" /><xsl:template match="Attachment[@Name='WidefocalExperimentSettings']" /></xsl:stylesheet>