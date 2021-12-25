from dataclasses import dataclass

# TODO: change all names into snake_case, convert to camel_case in serialiazer


@dataclass
class Part:
    name: str
    part: str
    year: str
    category: str = ""
    totalConvicted: int = None
    primaryLifeSentence: int = None
    primaryImprisonment: int = None
    primarySuspended: int = None
    primaryArrest: int = None
    primaryRestrain: int = None
    primaryRestrain2009: int = None
    primaryCorrectionalLabour: int = None
    primaryCommunityService: int = None
    primaryForcedLabour: int = None
    primaryFine: int = None
    primaryDisqualification: int = None
    primaryOther: int = None
    primaryMilitaryDisciplinaryUnit: int = None
    primaryRestrictionsInMilitaryService: int = None
    corruption: int = None
    primaryImprisonment1: int = None
    primaryImprisonment1_2: int = None
    primaryImprisonment1_3: int = None
    primaryImprisonment2_3: int = None
    primaryImprisonment3_5: int = None
    primaryImprisonment5_8: int = None
    primaryImprisonment8_10: int = None
    primaryImprisonment10_15: int = None
    primaryImprisonment15_20: int = None
    primaryImprisonmentUnderLowerLimit: int = None
    primaryFine5: int = None
    primaryFine5_25: int = None
    primaryFine25_100: int = None
    primaryFine25_500: int = None
    primaryFine100_300: int = None
    primaryFine300_500: int = None
    primaryFine500_1M: int = None
    primaryFine1M: int = None
    primaryFineSum: int = None
    exemptionAmnesty: int = None
    exemptionFromImprisonment: int = None
    exemptionOther: int = None
    acquittal: int = None
    dismissalAbsenceOfEvent: int = None
    dismissalAmnesty: int = None
    dismissalReconciliation: int = None
    dismissalRepentance: int = None
    dismissalCourtFine: int = None
    dismissalOther: int = None
    dismissalRepentance2: int = None
    dismissalCourtFine5: int = None
    dismissalCourtFine5_25: int = None
    dismissalCourtFine25_100: int = None
    dismissalCourtFine100: int = None
    dismissalCourtFineSum: int = None
    coerciveMeasures: int = None
    addDisqualification: int = None
    addFine: int = None
    addTitlesWithdraw: int = None
    addRestrain: int = None
    addFine5: int = None
    addFine5_25: int = None
    addFine25_500: int = None
    addFine25_100: int = None
    addFine100_300: int = None
    addFine300_500: int = None
    addFine500_1M: int = None
    addFine1M: int = None
    addFineSum: int = None
    unfinishedOffence: int = None
    noCrimeSelfdefence: int = None
    noCrimeNecessity: int = None
    noCrimeOther: int = None
    addTotalPersons: int = None
    addTotalOffences: int = None
    addAcquittalPersons: int = None
    addAcquittalOffences: int = None
    addDismissalPersons: int = None
    addDismissalOffences: int = None
    addDismissalOtherPersons: int = None
    addDismissalOtherOffences: int = None
    addUnfitToPleadPersons: int = None
    addUnfitToPleadOffences: int = None
    exemptionOtherGroundsFromImprisonment: int = None
    exemptionOtherGroundsOther: int = None
    exemptionAmnestyFromImprisonment: int = None
    exemptionAmnestyOther: int = None
    exemptionTimeServedFromImprisonment: int = None
    exemptionTimeServedOther: int = None
    addCoerciveMeasuresOffences: int = None


# статья
# часть
# параметр
# значение
# год

# статья состоит из частей
# номера частей неуникальны
# параметры варьируются год от года
# части можно складывать (т.е. значения соответствующих параметров друг с другом, но некоторые параметры при сложении дают неопределенное значение)
