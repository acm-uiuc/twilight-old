<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="8.3.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="meanwell_irm_v5">
<description>Meanwell OnBoard Power Supplies. Serie: IRM</description>
<packages>
<package name="IRM_15/20">
<wire x1="-26.2" y1="-13.6" x2="-26.2" y2="13.6" width="0.127" layer="21"/>
<wire x1="-26.2" y1="13.6" x2="26.2" y2="13.6" width="0.127" layer="21"/>
<wire x1="26.2" y1="13.6" x2="26.2" y2="-13.6" width="0.127" layer="21"/>
<wire x1="26.2" y1="-13.6" x2="-26.2" y2="-13.6" width="0.127" layer="21"/>
<text x="-2.54" y="1.27" size="1.27" layer="25">&gt;NAME</text>
<text x="-2.54" y="-2.54" size="1.27" layer="27">&gt;VALUE</text>
<pad name="AC/L" x="-22.8" y="-10.4" drill="1.3" diameter="2.54"/>
<pad name="AC/N" x="-22.8" y="10.4" drill="1.3" diameter="2.54"/>
<pad name="V-" x="22.2" y="-10.4" drill="1.3" diameter="2.54"/>
<pad name="V+" x="22.2" y="-2.4" drill="1.3" diameter="2.54"/>
<text x="-19.05" y="-10.16" size="1.27" layer="21">AC/L</text>
<text x="-19.05" y="8.89" size="1.27" layer="21">AC/N</text>
<text x="16.51" y="-2.54" size="1.27" layer="21">V+</text>
<text x="16.51" y="-11.43" size="1.27" layer="21">V-</text>
</package>
</packages>
<symbols>
<symbol name="IRM">
<wire x1="-10.16" y1="-10.16" x2="10.16" y2="-10.16" width="0.254" layer="94"/>
<wire x1="10.16" y1="-10.16" x2="10.16" y2="10.16" width="0.254" layer="94"/>
<wire x1="10.16" y1="10.16" x2="-10.16" y2="10.16" width="0.254" layer="94"/>
<wire x1="-10.16" y1="10.16" x2="-10.16" y2="-10.16" width="0.254" layer="94"/>
<pin name="AC/L" x="-12.7" y="-7.62" length="short" direction="in"/>
<pin name="AC/N" x="-12.7" y="7.62" length="short" direction="in"/>
<pin name="V+" x="12.7" y="7.62" length="short" direction="out" rot="R180"/>
<pin name="V-" x="12.7" y="-7.62" length="short" direction="out" rot="R180"/>
<text x="-7.62" y="12.7" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-15.24" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="IRM_15/20" uservalue="yes">
<description>&lt;b&gt;15 or 20 watt&lt;/b&gt; &lt;br/&gt;
housing &amp; pin compatible &lt;br/&gt;&lt;br/&gt;&lt;br/&gt;

&lt;b&gt;IRM 15&lt;/b&gt;
&lt;pre&gt;Vout [V]     Imax [A]     Pmax [W]     Eff [%]
3.3          3.5          11.55        74
5            3            15           78
12           1.25         15           82
15           1            15           82
24           0.63         15.12        83&lt;/pre&gt;&lt;br/&gt;&lt;br/&gt;&lt;br/&gt;

&lt;b&gt;IRM 20&lt;/b&gt;
&lt;pre&gt;Vout [V]     Imax [A]     Pmax [W]     Eff [%]
3.3          4.5          14.85        76
5            4            20           79
12           1.8          21.6         84
15           1.4          21.6         84
24           0.9          21.6         85&lt;/pre&gt;</description>
<gates>
<gate name="G$1" symbol="IRM" x="0" y="0"/>
</gates>
<devices>
<device name="" package="IRM_15/20">
<connects>
<connect gate="G$1" pin="AC/L" pad="AC/L"/>
<connect gate="G$1" pin="AC/N" pad="AC/N"/>
<connect gate="G$1" pin="V+" pad="V+"/>
<connect gate="G$1" pin="V-" pad="V-"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="wirepad" urn="urn:adsk.eagle:library:412">
<description>&lt;b&gt;Single Pads&lt;/b&gt;&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="3,81/1,4" urn="urn:adsk.eagle:footprint:30817/1" library_version="1">
<description>&lt;b&gt;THROUGH-HOLE PAD&lt;/b&gt;</description>
<wire x1="1.905" y1="-1.27" x2="1.905" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="1.905" y1="-1.905" x2="1.27" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="-1.905" x2="-1.905" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="-1.905" x2="-1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="1.27" x2="-1.905" y2="1.905" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="1.905" x2="-1.27" y2="1.905" width="0.1524" layer="21"/>
<wire x1="1.27" y1="1.905" x2="1.905" y2="1.905" width="0.1524" layer="21"/>
<wire x1="1.905" y1="1.905" x2="1.905" y2="1.27" width="0.1524" layer="21"/>
<circle x="0" y="0" radius="1.27" width="0.1524" layer="51"/>
<pad name="1" x="0" y="0" drill="1.397" diameter="3.81" shape="octagon"/>
<text x="-1.905" y="2.286" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="1.2" size="0.0254" layer="27">&gt;VALUE</text>
</package>
</packages>
<packages3d>
<package3d name="3,81/1,4" urn="urn:adsk.eagle:package:30835/1" type="box" library_version="1">
<description>THROUGH-HOLE PAD</description>
</package3d>
</packages3d>
<symbols>
<symbol name="PAD" urn="urn:adsk.eagle:symbol:30808/1" library_version="1">
<wire x1="-1.016" y1="1.016" x2="1.016" y2="-1.016" width="0.254" layer="94"/>
<wire x1="-1.016" y1="-1.016" x2="1.016" y2="1.016" width="0.254" layer="94"/>
<text x="-1.143" y="1.8542" size="1.778" layer="95">&gt;NAME</text>
<text x="-1.143" y="-3.302" size="1.778" layer="96">&gt;VALUE</text>
<pin name="P" x="2.54" y="0" visible="off" length="short" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="3,81/1,4" urn="urn:adsk.eagle:component:30853/1" prefix="PAD" uservalue="yes" library_version="1">
<description>&lt;b&gt;THROUGH-HOLE PAD&lt;/b&gt;</description>
<gates>
<gate name="1" symbol="PAD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="3,81/1,4">
<connects>
<connect gate="1" pin="P" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:30835/1"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="meanwell_irm_v5" deviceset="IRM_15/20" device=""/>
<part name="PAD1" library="wirepad" library_urn="urn:adsk.eagle:library:412" deviceset="3,81/1,4" device="" package3d_urn="urn:adsk.eagle:package:30835/1"/>
<part name="PAD2" library="wirepad" library_urn="urn:adsk.eagle:library:412" deviceset="3,81/1,4" device="" package3d_urn="urn:adsk.eagle:package:30835/1"/>
<part name="PAD3" library="wirepad" library_urn="urn:adsk.eagle:library:412" deviceset="3,81/1,4" device="" package3d_urn="urn:adsk.eagle:package:30835/1"/>
<part name="PAD4" library="wirepad" library_urn="urn:adsk.eagle:library:412" deviceset="3,81/1,4" device="" package3d_urn="urn:adsk.eagle:package:30835/1"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="25.4" y="12.7"/>
<instance part="PAD1" gate="1" x="5.08" y="20.32"/>
<instance part="PAD2" gate="1" x="5.08" y="5.08"/>
<instance part="PAD3" gate="1" x="45.72" y="20.32" rot="R180"/>
<instance part="PAD4" gate="1" x="45.72" y="5.08" rot="R180"/>
</instances>
<busses>
</busses>
<nets>
<net name="AC_N_IN" class="0">
<segment>
<pinref part="PAD1" gate="1" pin="P"/>
<pinref part="U$1" gate="G$1" pin="AC/N"/>
<wire x1="7.62" y1="20.32" x2="12.7" y2="20.32" width="0.1524" layer="91"/>
</segment>
</net>
<net name="AC_L_IN" class="0">
<segment>
<pinref part="PAD2" gate="1" pin="P"/>
<pinref part="U$1" gate="G$1" pin="AC/L"/>
<wire x1="7.62" y1="5.08" x2="12.7" y2="5.08" width="0.1524" layer="91"/>
</segment>
</net>
<net name="DC_LOW_OUT" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="V-"/>
<pinref part="PAD4" gate="1" pin="P"/>
<wire x1="38.1" y1="5.08" x2="43.18" y2="5.08" width="0.1524" layer="91"/>
</segment>
</net>
<net name="DC_HIGH_OUT" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="V+"/>
<pinref part="PAD3" gate="1" pin="P"/>
<wire x1="38.1" y1="20.32" x2="43.18" y2="20.32" width="0.1524" layer="91"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports the association of 3D packages
with devices in libraries, schematics, and board files. Those 3D
packages will not be understood (or retained) with this version.
</note>
</compatibility>
</eagle>
