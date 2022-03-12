"""Tests for EsptoolForm()"""

import re

from meshtastic_flasher.form import Form
from meshtastic_flasher.esptool_form import EsptoolForm, Worker


def test_EsptoolForm(qtbot):
    """Test EsptoolForm()"""
    f = Form()
    espf = EsptoolForm(f)
    qtbot.addWidget(f)
    qtbot.addWidget(espf)
    espf.start(port='foo', device_file='bar',
                 system_info_file='baz', bin_file='bam',
                 test=True)

def test_Worker_run_full(capsys):
    """Test Worker().run()"""
    a_worker = Worker(update_only=False, port='foo', device_file='bar',
                      system_info_file='baz', bin_file='bam',
                      test=True)
    a_worker.run()
    out, err = capsys.readouterr()
    assert re.search(r'Step 1/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 2/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 3/4 esp32 full', out, re.MULTILINE)
    assert re.search(r'Step 4/4 esp32 full', out, re.MULTILINE)
    assert err == ''


def test_Worker_run_update(capsys):
    """Test Worker().run()"""
    a_worker = Worker(update_only=True, port='foo', device_file='bar',
                      system_info_file='baz', bin_file='bam',
                      test=True)
    a_worker.run()
    out, err = capsys.readouterr()
    assert re.search(r'Step 1/2 esp32 update', out, re.MULTILINE)
    assert re.search(r'Step 2/2 esp32 update', out, re.MULTILINE)
    assert err == ''


def test_Worker_isatty():
    """Test Worker().isatty()"""
    a_worker = Worker(test=True)
    assert a_worker.isatty() is False


def test_update_status(qtbot):
    """Test update_status()"""
    f = Form()
    espf = EsptoolForm(f)
    qtbot.addWidget(f)
    qtbot.addWidget(espf)
    assert espf.status_label.text() != 'foo'
    espf.update_status('foo')
    assert espf.status_label.text() == 'foo'


def test_do_finished(qtbot):
    """Test do_finished()"""
    f = Form()
    espf = EsptoolForm(f)
    qtbot.addWidget(f)
    qtbot.addWidget(espf)
    assert espf.status_label.text() != ''
    assert espf.ok_button.isHidden() is True
    espf.do_finished()
    assert espf.status_label.text() == ''
    assert espf.ok_button.isHidden() is False


def test_receive_data(qtbot):
    """Test receive_data()"""
    f = Form()
    espf = EsptoolForm(f)
    qtbot.addWidget(f)
    qtbot.addWidget(espf)
    assert espf.text.toPlainText() == ''
    espf.receive_data('foo')
    assert espf.text.toPlainText() == 'foo'
    # ensure no blank lines are added
    espf.receive_data('\n')
    assert espf.text.toPlainText() == 'foo'
    espf.receive_data('bar\n')
    assert espf.text.toPlainText() == 'foo\nbar'
