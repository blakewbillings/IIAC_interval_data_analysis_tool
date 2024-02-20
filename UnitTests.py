from re import I
import pytest
from Dependencies.dataNormalizer import DataNormalizer 

# https://pytest.org/en/latest/getting-started.html#get-started
# Always add prefix: "test_" to answer
def func(x):
    return x+1

def f():
    raise SystemExit(1)

# For solution
def test_answer():
    assert func(3) == 4

# For raised Exception
def test_mytest():
    with pytest.raises(SystemExit):
        f()





# ===================== DateNormalizerTest =========================================
def test_normalizerPBC():
    #EXPECTED FORMAT = "%Y-%m-%d %H:%M:%S" 

    #PBC Electric 2019
    #Ex: 2019-01-01 00:00:00 MST | 2019-01-02 22:30:00 MST
    inputValues = ["2019-01-01 00:00:00 MST", "2019-01-02 22:30:00 MST"]
    expectedResult = ["2019-01-01 00:00:00", "2019-01-02 22:30:00"]
    for i in range(2):
            assert DataNormalizer.parseDateTime(inputValues[i]) == expectedResult[i]
    

def test_normalizerPacificorp():
    # Pacificorp format: "12/19/2022 0:15"
    inputValues = ["12/19/2022 0:15"]
    expectedResult = ["2022-12-19 00:15:00"]
    assert DataNormalizer.parseDateTime(inputValues[0]) == expectedResult[0]


def test_normalizerIPG():
    # IPG format: "1/1/2022 0:15" | "1/2/2022 18:45"
    inputValues = ["1/1/2022 0:15", "1/2/2022 18:45"]
    expectedResult = ["2022-01-01 00:15:00", "2022-01-02 18:45:00"]
    for i in range(2):
        assert DataNormalizer.parseDateTime(inputValues[i]) == expectedResult[i]


def test_normalizerBCMSL():
    # BCMSL format: "1/1/2019 0:30" | "1/5/2019 12:00"
    inputValues = ["1/1/2019 0:30", "1/5/2019 12:00"]
    expectedResult = ["2019-01-01 00:30:00", "2019-01-05 12:00:00"]
    for i in range(2):
        assert DataNormalizer.parseDateTime(inputValues[i]) == expectedResult[i]


def test_normalizerRMP():
    # RMP format: "1/1/2019 1830" | "1/2/2019 0015"
    inputValues = ["1/1/2019 1830", "1/2/2019 0015"]
    expectedResult = ["2019-01-01 18:30:00", "2019-01-02 00:15:00"]
    for i in range(2):
        assert DataNormalizer.parseDateTime(inputValues[i]) == expectedResult[i]


def test_normalizerExtra_TimeAsNum():
    # Extra1 format: "1/1/2019 15"
    inputValues = ["1/1/2019 15"]
    expectedResult = ["2019-01-01 00:15:00"]
    assert DataNormalizer.parseDateTime(inputValues[0]) == expectedResult[0]

def test_normalizerExtra_AM_PM():
    # AM/PM format: "1/1/2019 6:30PM" | "1/2/2019 1:15 AM"
    inputValues = ["1/1/2019 6:30PM" , "1/2/2019 1:15 AM"]
    expectedResult = ["2019-01-01 18:30:00", "2019-01-02 01:15:00"]
    for i in range(2):
        assert DataNormalizer.parseDateTime(inputValues[i]) == expectedResult[i]
        
def test_normalizerWith3Elements():
    # RMP-like format: "1/1/2019 00:00:00 1830"
    inputValues = ["1/1/2019 00:00:00 1830", "1/2/2019 00:00:00 0015"]
    expectedResult = ["2019-01-01 18:30:00", "2019-01-02 00:15:00"]
    for i in range(2):
        assert DataNormalizer.parseDateTime(inputValues[i]) == expectedResult[i]
def test_normalizerRMP_Special():
        inputValues = ["1/1/2019 00:00:00 2400"]
        expectedResult = ["2019-01-02 00:00:00"]
        assert DataNormalizer.parseDateTime(inputValues[0]) == expectedResult[0]
