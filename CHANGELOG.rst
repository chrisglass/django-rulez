Version 2.5
===========

* Django 1.4 compatibility fixes.
* New templatetag alows permission at user level.
* Various bugfixes.

Version 2.4
===========

* Various bugfixes

Version 2.3
===========

* Bugfix release

Version 2.2
===========

* Fixed cache warnings when using memcache: counters where computed using
  datetime.datetime, which generates whitespaces. It now uses time.time, which is
  a UNIX timestamp
* The unit tests system is now refactored, and running runtests.sh from the
  top-level directory should make the tests run.
* Test coverage was upped to about 93%


Version 2.0
============

* Added support for roles! See the code (sorry, no docs yet) to see how it's
  done
