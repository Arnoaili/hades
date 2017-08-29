#!/usr/bin/python
# -*- encoding: utf-8 -*-
from .utils import Storage

ITEM_FIELDS = (
    "1st Verified_SW 2 last Delivered",
    "Accept Change Requests",
    "Active Project Count",
    "Active Projects",
    "Active Test Sessions",
    "Active Work Items",
    "Actual Budget",
    "Actual Effort",
    "Actual Start Time",
    "Additional Comments",
    "Affect REQ",
    "All Content Count",
    "Allow Edits",
    "Allow Links",
    "Allow Model Owned Field Edits",
    "Allow Scope Expansion",
    "Allow Traces",
    "Annotation",
    "APK Name",
    "APK Release Type",
    "APK Status",
    "APK Version",
    "APP ID",
    "APP landscape",
    "APP Name",
    "APP Owner",
    "APP Release ID",
    "APP Release Version",
    "Artifact Affected",
    "Assigned Date",
    "Assignee Team Name",
    "Assignee E-Mail",
    "Assignee Department"
    "Assignee Telephone",
    "Assigned Group",
    "Assigned To",
    "Assigned to Verified_SW",
    "Assigned User",
    "At Risk Projects",
    "Attachments",
    "Author",
    "Authorized Change Count",
    "Authorizes Changes To",
    "Authorizing Change Order",
    "Author Reference Count In Active Projects",
    "Automated Behavior On Error",
    "Average Budget Variance",
    "Average Document Content Count",
    "Average Effort Variance",
    "Avg Close Time",
    "Avg SW Time",
    "Backward Affect REQ",
    "Backward Archive New Elements",
    "Backward Archive Reuse Elements",
    "Backward FR Branch Items",
    "Backward Related REQ",
    "Backward Relate FR",
    "Backward Relate SDM",
    "Backward Relate Task",
    "Backward Relate TC",
    "Backward Relationships",
    "Backward Reuse Create Items",
    "Belongs to Portfolio",
    "Belongs to Product",
    "Blocked",
    "Blocked By",
    "Blocking",
    "Blocks",
    "Bookmarks",
    "Branch",
    "singleBranch",
    "BR Relate FR",
    "Budget Variance",
    "Bug Category",
    "Bugzilla Database",
    "Bugzilla ID",
    "Build ID",
    "Burn Rate",
    "Business Devision",
    "Business Devision FVA",
    "Business Model",
    "Business Model FVA",
    "Category",
    "Category Int Value",
    "Cause",
    "CC",
    "Change Order Authorizations In Effect",
    "Change Order Count In Active Projects",
    "Change Order For",
    "Change Orders",
    "Change Package Count",
    "Change Package Entry Count",
    "Change Request Count",
    "Change Request Count In Active Projects",
    "Change Request For",
    "Change Request Phase",
    "Change Requests",
    "Change Requests For Project",
    "Changes Authorized",
    "Changes Authorized By",
    "Change Type",
    "Chapter Name",
    "City",
    "CKR",
    "Classification",
    "Clear Suspect",
    "Cloned Brother",
    "Cloned Brother1",
    "Closed Change Order Count",
    "Closed Change Order Count for Project",
    "Closed Change Requests",
    "Closed Date",
    "Last Time To Set Closed",
    "Closed Defect Count",
    "Closed Task Count",
    "Closed Test Objective Count",
    "Closed Test Session Count",
    "Closed Work Item Count",
    "Code Freeze Actual",
    "Code Freeze Current Estimate",
    "Code Freeze Original Estimate",
    "Code Name",
    "Coding Defects Slipped",
    "Comliance",
    "Comment For",
    "Comment From CEA",
    "Comment Text",
    "Completed Project Count",
    "Completed Projects",
    "Completed Test Sessions",
    "Component",
    "Contained By",
    "Contains",
    "Content Back Trace Count",
    "Content Count In Active Projects",
    "Content Fail Count",
    "Content Other Count",
    "Content Pass Count",
    "Content Run Count",
    "Content Without Back Traces Count",
    "Content Without Back Traces Percentage",
    "Cost Stability Index",
    "Created By",
    "Created Date",
    "CR relate FR",
    "CU REF",
    "Current Schedule",
    "customer milestone",
    "Date Completed",
    "Day Count",
    "Days in Current State",
    "Deadline",
    "Deadline Set Date",
    "Decomposed From",
    "Decomposes To",
    "Default CC",
    "Default value",
    "Defect For",
    "Defects",
    "DeResolution",
    "Description",
    "Design Defects Slipped",
    "Detected During",
    "Detection",
    "Development Complete Actual",
    "Development Complete Current Estimate",
    "Development Complete Original Estimate",
    "Development Plan",
    "Discussion",
    "Document Churn from Initial Baseline",
    "Document Count In Active Projects",
    "Documented By",
    "Document ID",
    "Document Phase",
    "Documents",
    "Documents Added Yesterday Count",
    "Document Short Title",
    "Documents Modified Yesterday Count",
    "Domain",
    "Downstream Trace Count",
    "DR0",
    "DR1",
    "DR2",
    "DR3",
    "DR4",
    "Duration for Assigned",
    "Duration Total Estimated Execution Time",
    "Editable",
    "Editable Value",
    "Effort",
    "Effort Variance",
    "Element CName",
    "End User Feedback",
    "End User Test Suggestion",
    "Eproject Flag",
    "Eproject Name",
    "Estimated Budget",
    "Estimated Effort",
    "Estimated Hours",
    "Estimated Time",
    "Execution place",
    "Execution Type",
    "Expected Results",
    "Exploratory Test Log",
    "External ID",
    "External Script Name",
    "Fail Count",
    "Feature Category",
    "Field",
    "First Target Project",
    "Forward Relationships",
    "FOTA Release Notes",
    "Found by Test Objective",
    "Found in Work Item",
    "FR Branch Items",
    "Frequency",
    "FR Relate Branch",
    "Function",
    "Functional Specification Freeze Actual",
    "Functional Specification Freeze Current Estimate",
    "Functional Specification Freeze Original Estimate",
    "Gerber Release for Mockup",
    "Global Active Project Count",
    "Global Completed Project Count",
    "Global Content Count",
    "Global Document Count",
    "Global Inactive Project Count",
    "Global Partially Satisfied Change Request Count",
    "Global Unallocated Change Request Count",
    "Green Project Count",
    "Green Project Count 2",
    "GUI",
    "Has Attachments",
    "Has Relationships",
    "Has Test Steps",
    "Health Value",
    "Health Value Range",
    "Heritability",
    "Hide",
    "Highest OS Support",
    "Homo",
    "Homo Yes Date",
    "Hours Worked",
    "ID",
    "Impacted Statement",
    "Inactive Project Count",
    "Inactive Projects",
    "Inactive Work Items",
    "Included Document Count",
    "Included Document Count in Project",
    "IncludeReference",
    "Include Subsegment in Metrics",
    "Inherited",
    "Initial Baseline",
    "Input Revision Date",
    "Inserted Document Count",
    "Inserted Document Count in Project",
    "In Session",
    "Interval For ASSIGNED",
    "Interval For DELIVERED",
    "Interval For NEW",
    "Interval For OPENED",
    "Interval For Postponed",
    "Interval For RESOLVED",
    "Interval For Verified",
    "Interval For Verified_SW",
    "Introduced During",
    "Investigation Target Date",
    "IPR Value",
    "Is Approval Comment",
    "isBranchCreate",
    "isModel",
    "isParent",
    "isCR",
    "Is Related To",
    "Is Supplier Test Case",
    "Item Significant Edit Date on Shared Item",
    "Keyword",
    "Keywords",
    "KO",
    "language",
    "Language List",
    "Last Delivered 2 Last Closed",
    "Lastest APK version REQ",
    "Last Result",
    "Last Verdict Type",
    "Last Verified_SW Date",
    "Last Week Document Churn",
    "Latest Apk Version",
    "Latest Release Version",
    "Lines of code",
    "Live Item ID",
    "LOT0",
    "LOT1",
    "LongTextReadOnly", #History Comments
    "Lowest OS Support",
    "Main Modification",
    "Major Version ID",
    "Managed By",
    "Managed Product Count",
    "Managed Project Count",
    "Managed Type",
    "Manages",
    "Manufacture Conform",
    "Manufacturer Comments",
    "Maximum Document Content Count",
    "Meaningful Content Count",
    "Member Count",
    "Members",
    "Milestone",
    "Minor Version ID",
    "Mockup",
    "Model Changed Date",
    "Model Description",
    "Model File",
    "Modelled By",
    "Modelling Tool",
    "Model Link",
    "Model Locked",
    "Model Reference",
    "Models",
    "Model Synchronize Date",
    "Model Synchronize Status",
    "Model Synchronize User",
    "Model Synchronize Version",
    "Model Type",
    "Modified By",
    "Modified Count Since Initial Baseline",
    "Modified Date",
    "Mozilla Due Date",
    "Mozilla Feature Type",
    "Mozilla Finish Date",
    "Mozilla ID",
    "Mozilla Issue Class",
    "Mozilla Last Update Filename",
    "Mozilla Project",
    "Mozilla Release",
    "Mozilla Solved in SW Release",
    "Mozilla Status",
    "MTK Action",
    "MTK Bug Category",
    "MTK Due Date",
    "MTK Feature Type",
    "MTK Finish Date",
    "MTK Issue Class",
    "MTK Issue ID",
    "MTK Issue Type",
    "MTK Last Update Filename",
    "MTK Modem Project",
    "MTK Modem Version",
    "MTK Platform",
    "MTK Project",
    "MTK Release",
    "MTK Release Type",
    "MTK Resolution",
    "MTK Solved In SW Release",
    "MTK Status",
    "MVNO DO",
    "MVNO DV",
    "Name",
    "Need Notification",
    "Needs New Changes",
    "New Estimated Due Date",
    "New Ref",
    "New to Verified_SW",
    "Next Ref",
    "Notification Receive Groups",
    "Notification Receive Users",
    "Open And Pending Defect Count",
    "Open Change Order Count",
    "Open Change Order Count for Project",
    "Open Change Package Count",
    "Open Defect Count",
    "Open Task Count",
    "Open Test Objective Count",
    "Open Test Session Count",
    "Open Work Item Count",
    "Operator Acceptance",
    "Operator Comments",
    "Operator Name",
    "Operators",
    "Operator Test Case ID",
    "Optional Fields",
    "OR",
    "Orange Check Repeat",
    "Orange ID",
    "Orange Info",
    "Orange Project",
    "Order",
    "Original Brother",
    "Original Brother1",
    "Original Schedule",
    "Originator",
    "Orphaned Node Count",
    "Orphaned Shared Item Count",
    "OS",
    "OS Support",
    "OS Version",
    "Other Count",
    "Outstanding Change Request Count",
    "Package Name",
    "Parameters",
    "Parameters From Shared Item",
    "Parameter Values",
    "Parameter Values From Shared Item",
    "Parent",
    "Parent Clone",
    "Pass Count",
    "path",
    "Pending Change Order Count",
    "Pending Defect Count",
    "Pending Task Count",
    "Pending Test Objective Count",
    "Pending Test Session Count",
    "Pending Work Item Count",
    "Perso ID",
    "PIO",
    "PIO2",
    "Planned Count",
    "Planned End Date",
    "Planned Start Date",
    "Planned Start Time",
    "Platform",
    "Platform Comments",
    "Platform Conform",
    "Platform PR ID",
    "Platform Type",
    "Platform Version",
    "Possible values(METATYPE)",
    "Post Branch Edit",
    "Postponed Release",
    "Preconditions",
    "Priority",
    "Process Category",
    "Product",
    "Product Health Value",
    "Product Health Value Range",
    "Product Manager",
    "Product Parameters",
    "Product Type",
    "Product Type FVA",
    "Project",
    "Project Acceptance Actual",
    "Project Acceptance Current Estimate",
    "Project Acceptance Original Estimate",
    "Project Allow Scope Expansion",
    "Project Branch",
    "Project Classification",
    "projectIBPL",
    "Project Plan Actual",
    "Project Plan Current Estimate",
    "Project Plan Original Estimate",
    "Project Requires Change Orders",
    "Project Start Actual",
    "Project Start Current Estimate",
    "Project Start Original Estimate",
    "Project State",
    "Proposed Project Count",
    "Proposed Projects",
    "Proposed Work Items",
    "Proto",
    "PR Report Time",
    "PR Sharing Type",
    "QCT Associated Baseband Chip",
    "QCT Build Id",
    "QCT Problem Code",
    "QCT Product",
    "QCT Request Number",
    "QCT Request Type",
    "QCT Status",
    "Reason for Not compilance",
    "Record Results As Shared",
    "Red Project Count",
    "Red Project Count 2",
    "Referenced Bookmarks",
    "Referenced By",
    "Referenced Item Type",
    "Reference Document",
    "Reference Mode",
    "References",
    "Regression",
    "Regression Comment",
    "Regression Response",
    "Regression Set Date",
    "Relate CR",
    "Related Project",
    "Related REQ",
    "Relate FR",
    "Relate Milestone",
    "Relate SDM",
    "Relate Task",
    "Relate TC",
    "Related UTC",
    "Relationship Flags",
    "Release",
    "Release Note",
    "Remove selected CCs",
    "Repeated",
    "Repeated Defect ID",
    "Repeated TaskID",
    "Reported By",
    "REQ Category",
    "REQ Document Type",
    "Requireement Info",
    "Requirement Count",
    "Requirement Count Change",
    "Requirement Count from Initial Baseline",
    "Requirement Defects Slipped",
    "Requirements",
    "Requirement Stability Index",
    "Requirement Title",
    "Requires Validation",
    "REQ Version No",
    "Resolution",
    "Resolved By",
    "Retired States",
    "Reuse Create Items",
    "Reuse Reference Count In Active Projects",
    "Review Session For",
    "Review Sessions",
    "Revision",
    "Revision Increment Date",
    "Roadmap Year",
    "Roadmap Year FVA",
    "Root Cause Category",
    "Root Document",
    "Root ID",
    "Row",
    "Run Count",
    "Running Cost",
    "Run Percentage",
    "Satisfied By",
    "Satisfies",
    "Schedule Stability Index",
    "Screen Autofit",
    "SDM/RDM ID",
    "Section",
    "Section Name",
    "Selection Index",
    "Session Type",
    "Severity",
    "SH APP",
    "Shared Attachments",
    "Shared Automated Behavior On Error",
    "Shared By",
    "Shared Category",
    "Shared Expected Results",
    "Shared External ID",
    "Shared External Script Name",
    "Shared Model Changed Date",
    "Shared Model Description",
    "Shared Model Link",
    "Shared Model Reference",
    "Shared Model Type",
    "Shared Test Steps",
    "Shared Text",
    "Share Reference Count In Active Projects",
    "Shares",
    "Shares Test Case",
    "ShareUseInteger1",
    "ShareUseInteger2",
    "ShareUseInteger3",
    "ShareUseInteger4",
    "ShareUseInteger5",
    "SH FT Team",
    "Show In Finder",
    "SH Perso Team",
    "SH Telecom",
    "SH Tool",
    "Signature Comment",
    "Signed By",
    "Significant Change Since Item Revision",
    "Significant Edit Date",
    "Simulated Model",
    "Site",
    "Site FVA",
    "Solution",
    "Solution Time Gap",
    "Solving Release",
    "Source Checkpoint Count",
    "Source File Count",
    "Source Project",
    "Source Subproject Count",
    "Spawned By",
    "Spawns",
    "Specification Count",
    "Stakeholders",
    "State",
    "Status Report",
    "Step Actions",
    "Stock DO",
    "Stock DV",
    "Structure",
    "Structure Type",
    "Submitter Site",
    "Sub Module",
    "Sub Section Name",
    "Subsegment Name",
    "Summary",
    "Supplier",
    "Suspect Content Count",
    "Suspect Content Percentage",
    "Suspect Content Percentage In Project",
    "Suspect Count",
    "Suspect Relationship Count",
    "Suspect Results",
    "SW Patch Target Date",
    "SW Patch Target Set Date",
    "SW Purpose",
    "SW Release",
    "SW Version",
    "Tablet Version",
    "Task Phase",
    "TCT HW Project",
    "Team",
    "Teleweb Version",
    "Test Case",
    "Test Case Count",
    "Test Case Editable",
    "Test Case ID",
    "Test Case Module",
    "Test Case Name",
    "Test Case Related Test Suite",
    "Test Cases",
    "Test Change Orders",
    "Tested By",
    "Test Environment",
    "test fva",
    "test fvaa",
    "TestMultiUser",
    "Test Objective",
    "Test Objective Blocked Count",
    "Test Objective Fail Count",
    "Test Objective For",
    "Test Objective Other Count",
    "Test Objective Pass Count",
    "Test Objective Phase",
    "Test Objective Planned Count",
    "Test Objective Run Count",
    "Test Objectives",
    "Test Objective Suspect Results Count",
    "Test of",
    "Test Plan For",
    "Test Plan Related Test Strategies",
    "Test Plans",
    "Test Reference",
    "Test Relevant",
    "Test Result Attachment",
    "Test Result Modified Date",
    "Test Result Modified User",
    "Tests",
    "Tests As Of Date",
    "Tests As of Date Count",
    "Tests As Of Date Set",
    "Test Session",
    "Test Session Phase",
    "Test Session Tests Count",
    "Tests For",
    "Test Step Editable",
    "Test Steps",
    "Test Step Test Cases Count",
    "Test Strategy Related Test Plan",
    "Test Strategy Related Test Suites",
    "Test Strategy Value",
    "Test Suite Count",
    "Test Suite Related Test Cases",
    "Test Suite Related Test Strategy",
    "Test Tool",
    "Text",
    "Text Attachments",
    "Time To Set Assigned",
    "Time To Set Delivered",
    "Time To Set New",
    "Time To Set Open",
    "Time To Set Resolved",
    "Time To Set Verified",
    "Time To Set Verified_SW",
    "Top Level Document Count",
    "Total Actual Budget",
    "Total Actual Effort",
    "Total Blocked Count",
    "Total Budget Variance",
    "Total Budget Variance Range",
    "Total Change Order Count",
    "Total Change Package Count",
    "Total Change Package Entry Count",
    "Total Content Fail Count",
    "Total Content Other Count",
    "Total Content Pass Count",
    "Total Content Run Count",
    "Total Defect Count",
    "Total Effort Variance",
    "Total Effort Variance Range",
    "Total Estimated Budget",
    "Total Estimated Effort",
    "Total Fail Count",
    "Total Open Change Package Count",
    "Total Other Count",
    "Total Pass Count",
    "Total Pass Percentage of Planned",
    "Total Pass Percentage of Run",
    "Total Planned Count",
    "Total Remaining Effort",
    "Total Run Count",
    "Total Run Percentage",
    "Total Suspect Results Count",
    "Total Task Count",
    "Total Test Objective Count",
    "Total Test Session Count",
    "Total Work Item Count",
    "Trace Status",
    "TSR",
    "Type",
    "Unallocated Change Request Count",
    "Uninstall",
    "Unique ID",
    "Unsatisfied Requirements Percentage",
    "Untraced Content Percentage",
    "Untraced Inputs Percentage",
    "Unused Computed Logical 1",
    "Unused Computed Logical 2",
    "Unused Int1",
    "Unused Int2",
    "Unverified Requirements Percentage",
    "Upstream Trace Count",
    "Use Hierarchical Editability",
    "UTC Required?",
    "Validated By",
    "Validated By Pass Count",
    "Validated By Pass Percentage",
    "Validated By Trace Count",
    "Validated By Trace Health",
    "Validates",
    "Valid Change Order",
    "Valid Test Step Change Order",
    "VAL Phase",
    "VAL Refuse",
    "Val Refused Date",
    "Variety",
    "Verdict",
    "Verdict Icon",
    "Verdict Type",
    "Verdict Type Icon",
    "Verified By",
    "Verified By Pass Count",
    "Verified By Pass Percentage",
    "Verified By Trace Count",
    "Verified By Trace Health",
    "Verified_SW Date",
    "Verified_SW to Closed",
    "Verifier",
    "Verifies",
    "Version",
    "Widget linked",
    "Work Item",
    "Work Item For",
    "Work Item Phase",
    "Work Items",
    "Yellow Project Count",
    "Yellow Project Count 2",
    "Yesterday Document Churn")

class IntegrityItem(Storage):
    type = "IntegrityItem"
    fields = ITEM_FIELDS

    def __eq__(self, a):
        return self.id == a.id

    @property
    def assigned_user(self):
        ret = Storage()
        ret.user = ''
        ret.fullname = ''
        ret.email = ''
        if 'Assigned User' in self.keys():
            # there only one assigned user for each item ???
            record = self['Assigned User'].UserRecord[0]
            try:
                ret.user = record.user.value
            except AttributeError:
                ret.user = ""
            try:
                ret.fullname = record.fullname.value
            except AttributeError:
                ret.fullname = ""
            try:
                ret.email = record.email.value
            except AttributeError:
                ret.email = ""
            return ret
        return None

    @property
    def state(self):
        try:
            return self['state']
        except KeyError:
            if 'State' in self.keys():
                return self['State'].state
        return ''

    @property
    def description(self):
        if 'Description' in self.keys():
            return self['Description'][1].value
        return ''

    @property
    def summary(self):
        if 'Summary' in self.keys():
            return self['Summary'][1].value
        return ''

    @property
    def project(self):
        if 'Project' in self.keys():
            return self['Project'].project.value
        return ''

    @property
    def created_date(self):
        if 'Created Date' in self.keys():
            return self['Created Date'].dateTime.value
        return ''

    @property
    def modified_date(self):
        if 'Modified Date' in self.keys():
            return self['Modified Date'].dateTime.value
        return ''

#########Add By LuoLu################
##########add closed_date###########
    @property
    def closed_date(self):
        if 'Last Time To Set Closed' in self.keys():
            return self['Last Time To Set Closed'].dateTime.value
        return ''

#########add deadline###########
    @property
    def deadline(self):
        if 'Deadline' in self.keys():
            return self['Deadline'].date.value
        return ''

########add val refuse#########
    @property
    def val_refuse(self):
        if 'VAL Refuse' in self.keys():
            return self['VAL Refuse'].shorttext.value
        return ''

########add sw release#########
    @property
    def sw_release(self):
        if 'SW Release' in self.keys():
            return self['SW Release']
        return ''

########add Regression#########
    @property
    def regression(self):
        if 'Regression' in self.keys():
            return self['Regression'].shorttext.value
        return ''


########add milestone##########
    @property
    def milestone(self):
        if 'Milestone' in self.keys():
            return self['Milestone']
        return ''


########End By LuoLu###############

#########Add By Yangmei################
    @property
    def assigned_date(self):
        if 'Time To Set Assigned' in self.keys():
            return self['Time To Set Assigned'].dateTime.value
        return ''

    @property
    def refused_date(self):
        if 'Val Refused Date' in self.keys():
            return self['Val Refused Date'].date.value
        return ''

    @property
    def homo(self):
        if 'Homo' in self.keys():
            return self['Homo'].shorttext.value
        return ''

    @property
    def regression_date(self):
        if 'Regression Set Date' in self.keys():
            return self['Regression Set Date'].date.value
        return ''

    @property
    def assigned_team(self):
        if 'Assignee Team Name' in self.keys():
            return self['Assignee Team Name'][1].value
        return ''

    @property
    def assigned_email(self):
        if "Assignee E-Mail" in self.keys():
            return self['Assignee E-Mail'].shorttext.value
        return ''

    @property
    def assigned_department(self):
        if "Assignee Department" in self.keys():
            return self['Assignee Department'].shorttext.value
        return ''

    @property
    def assigned_telephone(self):
        if "Assignee Telephone" in self.keys():
            return self['Assignee Telephone'].shorttext.value
        return ''

    @property
    def isCR(self):
        if "isCR" in self.keys():
            return self['isCR'].boolean.value
        return ''
########End By Yangmei###############
########Add By Aili############
    @property
    def verified_sw_date(self):
        if 'Last Verified_SW Date' in self.keys():
            return self['Last Verified_SW Date'].dateTime.value
        return ''

    @property
    def new_date(self):
        if 'Time To Set New' in self.keys():
            return self['Time To Set New'].dateTime.value
        return ''

    @property
    def resolver(self):
        if 'Resolved By' in self.keys():
            return self['Resolved By'].shorttext.value
        return ''

    @property
    def long_text_read_only(self):
        if 'LongTextReadOnly' in self.keys():
            return self['LongTextReadOnly'].longtext.value
        return ''

#########END##############
    @property
    def function(self):
        if 'Function' in self.keys():
            return self['Function'][1].value
        return ''

    @property
    def reporter(self):
        ret = Storage()
        ret.user = ''
        ret.fullname = ''
        ret.email = ''
        if 'Reported By' in self.keys():
            # there only one assigned user for each item ???
            record = self['Reported By'].UserRecord[0]
            try:
                ret.user = record.user.value
            except AttributeError:
                ret.user = ""
            try:
                ret.fullname = record.fullname.value
            except AttributeError:
                ret.fullname = ""
            try:
                ret.email = record.email.value
            except AttributeError:
                ret.email = ""
            return ret
        return None

    @property
    def new_ref(self):
        if 'New Ref' in self.keys():
            return self['New Ref'][1].value
        return ''

    @property
    def resolution(self):
        if 'Resolution' in self.keys():
            return self['Resolution'][1].value
        return ''

    @property
    def name(self):
        if 'Name' in self.keys():
            return self['Name'][1].value
        return ''

    @property
    def branch(self): # branch is a RelatedItem
        if 'singleBranch' in self.keys():
            return self['singleBranch'][1].value  ## it's a string here
        if 'Branch' in self.keys():
            return self['Branch'][1].value  ## it's a list here
        return ''

    @property
    def comment_from_cea(self):
        if 'Comment From CEA' in self.keys():
            return self['Comment From CEA'][1].value
        return ''

    @property
    def last_verified_sw_date(self):
        if 'Last Verified_SW Date' in self.keys():
            return self['Last Verified_SW Date'][1].value
        return ''

    @property
    def ipr_value(self):
        if 'IPR Value' in self.keys():
            return self['IPR Value'][1].value
        return 0

    @property
    def priority(self):
        if 'Priority' in self.keys():
            return self['Priority'][1].value
        return ''

    def __repr__(self):
        return '<%s %s>' % (self.__class__.type, str(self.id))

class APKRelease(IntegrityItem):
    type = "APK Release"


class ArchiveItem(IntegrityItem):
    type = "Archive Item"


class CR(IntegrityItem):
    type = "CR"


class Task(IntegrityItem):
    type = "Task"

class StabilityDefect(IntegrityItem):
    type = 'Stability Defect'

class Team(IntegrityItem):
    type = "Team"


class TestCC(IntegrityItem):
    type = "Test CC"


class TestType(IntegrityItem):
    type = "Test Type"


class Defect(IntegrityItem):
    type = "Defect"


class ChangeOrder(IntegrityItem):
    type = "Change Order"


class ChangeRequest(IntegrityItem):
    type = "Change Request"


class Library(IntegrityItem):
    type = "Library"


class MKSSolution(IntegrityItem):
    type = "MKS Solution"


class Portfolio(IntegrityItem):
    type = "Portfolio"


class Product(IntegrityItem):
    type = "Product"


class Project(IntegrityItem):
    type = "Project"

    @property
    def name(self):
        return getattr(self, 'Name', '')


class Simulation(IntegrityItem):
    type = "Simulation"


class TestObjective(IntegrityItem):
    type = "Test Objective"


class TestPlan(IntegrityItem):
    type = "Test Plan"


class TestSession(IntegrityItem):
    type = "Test Session"


class TestStep(IntegrityItem):
    type = "Test Step"


class WorkItem(IntegrityItem):
    type = "Work Item"


class Requirement(IntegrityItem):
    type = "Requirement"


class RequirementDocument(IntegrityItem):
    type = "Requirement Document"


class GeneralSystemRequirement(IntegrityItem):
    type = "General System Requirement"


class GeneralSystemRequirementDocument(IntegrityItem):
    type = "General System Requirement Document"


class GeneralFunctionalRequirementDocument(IntegrityItem):
    type = "General Functional Requirement Document"


class GeneralFunctionalRequirement(IntegrityItem):
    type = "General Functional Requirement"


class testConstraints(IntegrityItem):
    type = "testConstraints"


class TestSuite(IntegrityItem):
    type = "Test Suite"


class TestCase(IntegrityItem):
    type = "Test Case"


class Branch(IntegrityItem):
    type = "Branch"

class ReleaseNote(IntegrityItem):
    type = "Release Note"

    @property
    def version(self):
        if 'Version' in self.keys():
            #return self['Version'][1].value
            return self['Version']
        return ""

class MTKDefect(IntegrityItem):
    type = "MTK Defect"

class QCTDefect(IntegrityItem):
    type = "QCT Defect"

class Patch(IntegrityItem):
    type = "Patch"

class MozillaDefect(IntegrityItem):
    type = "Mozilla Defect"

class OperatorFunctionalRequirement(IntegrityItem):
    type = "Operator Functional Requirement"

class OperatorSystemRequirement(IntegrityItem):
    type = "Operator System Requirement"

class OrangeDefect(IntegrityItem):
    type = "Orange Defect"

class Assignment(IntegrityItem):
    type = "Assignment"

class UserItem(Storage):
    type = "User Item"

    @property
    def name(self):
        if 'Assigned User' in self.keys():
            return self['Assigned User']['UserRecord'][0].user.value
        return ''

    @property
    def fullname(self):
        if 'Assigned User' in self.keys():
            return self['Assigned User']['UserRecord'][0].fullname.value
        return ''

    @property
    def email(self):
        if 'Assigned User' in self.keys():
            return self['Assigned User']['UserRecord'][0].email.value
        return ''

    @property
    def telephone(self):
        if 'Telephone' in self.keys():
            return self['Telephone'][1].value
        return ''

    @property
    def teamname(self):
        if 'Team Name' in self.keys():
            return self['Team Name'][1].value
        return ''

    @property
    def department(self):
        if 'Department' in self.keys():
            return self['Department'][1].value
        return ''

    def __repr__(self):
        return '<%s>' % (self.fullname)

class OperatorFR(IntegrityItem):
    type = "Operator FR"

class GeneralFR(IntegrityItem):
    type = "General FR"

class SDM(IntegrityItem):
    type = "SDM"

    @property
    def metatype(self):
        if 'Possible values(METATYPE)' in self.keys():
            return self['Possible values(METATYPE)'][1].value
        return ''

    @property
    def sdm_id(self):
        if 'SDM/RDM ID' in self.keys():
            return self['SDM/RDM ID'][1].value
        return ''

class FRBranch(IntegrityItem):
    type = "FR Branch"
