from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper

from dostoevsky import model

# TODO: CHange "noCrimeSelf-defence" to "noCrimeSelfdefence" in https://github.com/goooseman/dostoevsky-website/blob/develop/content/metri%D1%81s.json

metadata = MetaData()

parts = Table(
    "parts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("part", String(20), nullable=False),
    Column("year", String(4), nullable=False),
    Column("category", String(255), default="", server_default="", nullable=False),
    Column("totalConvicted", Integer, nullable=True),
    Column("primaryLifeSentence", Integer, nullable=True),
    Column("primaryImprisonment", Integer, nullable=True),
    Column("primarySuspended", Integer, nullable=True),
    Column("primaryArrest", Integer, nullable=True),
    Column("primaryRestrain", Integer, nullable=True),
    Column("primaryRestrain2009", Integer, nullable=True),
    Column("primaryCorrectionalLabour", Integer, nullable=True),
    Column("primaryCommunityService", Integer, nullable=True),
    Column("primaryForcedLabour", Integer, nullable=True),
    Column("primaryFine", Integer, nullable=True),
    Column("primaryDisqualification", Integer, nullable=True),
    Column("primaryOther", Integer, nullable=True),
    Column("primaryMilitaryDisciplinaryUnit", Integer, nullable=True),
    Column("primaryRestrictionsInMilitaryService", Integer, nullable=True),
    Column("corruption", Integer, nullable=True),
    Column("primaryImprisonment1", Integer, nullable=True),
    Column("primaryImprisonment1_2", Integer, nullable=True),
    Column("primaryImprisonment1_3", Integer, nullable=True),
    Column("primaryImprisonment2_3", Integer, nullable=True),
    Column("primaryImprisonment3_5", Integer, nullable=True),
    Column("primaryImprisonment5_8", Integer, nullable=True),
    Column("primaryImprisonment8_10", Integer, nullable=True),
    Column("primaryImprisonment10_15", Integer, nullable=True),
    Column("primaryImprisonment15_20", Integer, nullable=True),
    Column("primaryImprisonmentUnderLowerLimit", Integer, nullable=True),
    Column("primaryFine5", Integer, nullable=True),
    Column("primaryFine5_25", Integer, nullable=True),
    Column("primaryFine25_100", Integer, nullable=True),
    Column("primaryFine25_500", Integer, nullable=True),
    Column("primaryFine100_300", Integer, nullable=True),
    Column("primaryFine300_500", Integer, nullable=True),
    Column("primaryFine500_1M", Integer, nullable=True),
    Column("primaryFine1M", Integer, nullable=True),
    Column("primaryFineSum", Integer, nullable=True),
    Column("exemptionAmnesty", Integer, nullable=True),
    Column("exemptionFromImprisonment", Integer, nullable=True),
    Column("exemptionOther", Integer, nullable=True),
    Column("acquittal", Integer, nullable=True),
    Column("dismissalAbsenceOfEvent", Integer, nullable=True),
    Column("dismissalAmnesty", Integer, nullable=True),
    Column("dismissalReconciliation", Integer, nullable=True),
    Column("dismissalRepentance", Integer, nullable=True),
    Column("dismissalCourtFine", Integer, nullable=True),
    Column("dismissalOther", Integer, nullable=True),
    Column("dismissalRepentance2", Integer, nullable=True),
    Column("dismissalCourtFine5", Integer, nullable=True),
    Column("dismissalCourtFine5_25", Integer, nullable=True),
    Column("dismissalCourtFine25_100", Integer, nullable=True),
    Column("dismissalCourtFine100", Integer, nullable=True),
    Column("dismissalCourtFineSum", Integer, nullable=True),
    Column("coerciveMeasures", Integer, nullable=True),
    Column("addDisqualification", Integer, nullable=True),
    Column("addFine", Integer, nullable=True),
    Column("addTitlesWithdraw", Integer, nullable=True),
    Column("addRestrain", Integer, nullable=True),
    Column("addFine5", Integer, nullable=True),
    Column("addFine5_25", Integer, nullable=True),
    Column("addFine25_500", Integer, nullable=True),
    Column("addFine25_100", Integer, nullable=True),
    Column("addFine100_300", Integer, nullable=True),
    Column("addFine300_500", Integer, nullable=True),
    Column("addFine500_1M", Integer, nullable=True),
    Column("addFine1M", Integer, nullable=True),
    Column("addFineSum", Integer, nullable=True),
    Column("unfinishedOffence", Integer, nullable=True),
    Column("noCrimeSelfdefence", Integer, nullable=True),
    Column("noCrimeNecessity", Integer, nullable=True),
    Column("noCrimeOther", Integer, nullable=True),
    Column("addTotalPersons", Integer, nullable=True),
    Column("addTotalOffences", Integer, nullable=True),
    Column("addAcquittalPersons", Integer, nullable=True),
    Column("addAcquittalOffences", Integer, nullable=True),
    Column("addDismissalPersons", Integer, nullable=True),
    Column("addDismissalOffences", Integer, nullable=True),
    Column("addDismissalOtherPersons", Integer, nullable=True),
    Column("addDismissalOtherOffences", Integer, nullable=True),
    Column("addUnfitToPleadPersons", Integer, nullable=True),
    Column("addUnfitToPleadOffences", Integer, nullable=True),
    Column("exemptionOtherGroundsFromImprisonment", Integer, nullable=True),
    Column("exemptionOtherGroundsOther", Integer, nullable=True),
    Column("exemptionAmnestyFromImprisonment", Integer, nullable=True),
    Column("exemptionAmnestyOther", Integer, nullable=True),
    Column("exemptionTimeServedFromImprisonment", Integer, nullable=True),
    Column("exemptionTimeServedOther", Integer, nullable=True),
    Column("addCoerciveMeasuresOffences", Integer, nullable=True),
)


def start_mappers():
    parameters_mapper = mapper(model.Part, parts)