#!/usr/bin/perl

# Author     Version      Date        Comments
# FQuinto    1.0.0        2015-Nov    First version fron NoConName 2015 event

# RRd data generation
# Copyright (C) 2015 Fran Quinto

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

use RRDs;

# define location of rrdtool databases
my $rrd = '/opt';
# define location of images
my $img = '/var/www';

while ($value eq '') {
	$value=`/usr/bin/python /home/pi/temphum.py`;
	($temperature,$humidity) = split(',', $value);
	($aux,$temperature) = split(':', $temperature);
	($aux,$humidity) = split(':', $humidity);
	$temperature =~ s/[\n ]//g; # remove eol chars and white space
	$humidity =~ s/[\n ]//g; # remove eol chars and white space
}
&DHT22("Temperature",$temperature);
&DHT22("Humidity",$humidity);

sub DHT22
{
# process DHT22 sensor
# inputs: $_[0]: Temperature or Humidity
# inputs: $_[1]: Value (Temperature or Humidity)
    my $value="";
	if ($_[0] eq "Humidity")
	{
		$value = $_[1];
		$value_type = "humid";
		$min = "0";
	    $max = "100"; #%
	}
	elsif ($_[0] eq "Temperature")
	{
		$value = $_[1];
		$value_type = "temp";
	    $min = "-5";
	    $max = "45";
	}

	print "$_[0] (DHT22): $value\n";

	# if rrdtool database doesn't exist, create it
	if (! -e "$rrd/$_[0].rrd")
	{
		print "creating rrd database for $_[0]...\n";
		RRDs::create "$rrd/$_[0].rrd",
			"-s 60",
			"DS:$value_type:GAUGE:300:$min:$max",
			"RRA:AVERAGE:0.5:1:60",
			"RRA:AVERAGE:0.5:6:240",
			"RRA:AVERAGE:0.5:12:840",
			"RRA:AVERAGE:0.5:24:1830",
			"RRA:AVERAGE:0.5:144:3660";
	}

	# insert value into rrd
	RRDs::update "$rrd/$_[0].rrd",
		"-t", "$value_type",
		"N:$value";

	# create graphs
	&CreateGraph($_[0], "hour");
	&CreateGraph($_[0], "day");
	&CreateGraph($_[0], "week");
	&CreateGraph($_[0], "month");
	&CreateGraph($_[0], "year");
}

sub CreateGraph
{
# creates graph
# inputs: $_[0]: Temperature or Humidity
#         $_[1]: interval (ie, day, week, month, year)

	if ($_[0] eq "Humidity")
	{
		RRDs::graph "$img/$_[0]-$_[1].png",
		"--lazy",
		"-s -1$_[1]",
		"-t DHT22 :: $_[0]",
		"-h", "80", "-w", "600",
		"-a", "PNG",
		"-v Percent Humidity",
		"DEF:humid=$rrd/$_[0].rrd:humid:AVERAGE",
		"LINE2:humid#4d3499:$_[0] ($_[0])",
		"GPRINT:humid:MIN:  Min\\: %3.1lf%%",
		"GPRINT:humid:MAX: Max\\: %3.1lf%%",
		"GPRINT:humid:AVERAGE: Avg\\: %3.1lf%%",
		"GPRINT:humid:LAST: Current\\: %3.1lf%%\\n";
	}
	elsif ($_[0] eq "Temperature")
	{
		RRDs::graph "$img/$_[0]-$_[1].png",
		"--lazy",
		"-s -1$_[1]",
		"-t DHT22 :: $_[0]",
		"-h", "80", "-w", "600",
		"-a", "PNG",
		"-v degrees °C",
		"DEF:temp=$rrd/$_[0].rrd:temp:AVERAGE",
		"LINE2:temp#aa3f4a:$_[0] ($_[0])",
		"GPRINT:temp:MIN:  Min\\: %2.1lf°C",
		"GPRINT:temp:MAX: Max\\: %2.1lf°C",
		"GPRINT:temp:AVERAGE: Avg\\: %4.1lf°C",
		"GPRINT:temp:LAST: Current\\: %2.1lf°C\\n";
	}


	if ($ERROR = RRDs::error) { print "$0: unable to generate $_[0] graph: $ERROR\n"; }
}
