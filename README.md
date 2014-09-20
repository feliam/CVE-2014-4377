CoreGraphics Memory Corruption - CVE-2014-4377
==============================================

Apple CoreGraphics library fails to validate the input when parsing the colorspace specification of a PDF XObject resulting in a heap overflow condition. A small heap memory allocation can be overflowed with controlled data from the input in any application linked with the affected framework. Using a crafted PDF file as an HTML image and combined with a information leakage vulnerability this issue leads to arbitrary code execution. A complete 100% reliable and portable exploit for MobileSafari on IOS7.1.x. can be downloaded from github 

Summary
========
* Title: Apple CoreGraphics Memory Corruption
* CVE Name: CVE-2014-4377
* Permalink: http://blog.binamuse.com/2014/09/coregraphics-memory-corruption.html
* Date published: 2014-09-18
* Date of last update: 2014-09-19
* Class: Client side / Integer Overflow / Memory Corruption
* Advisory: HT6441 HT6443

