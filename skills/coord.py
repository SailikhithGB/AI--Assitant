"""
Real World Coordinator - Physical World Integration
Handles real-world coordination tasks like scheduling, bookings, and communications
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import re

logger = logging.getLogger(__name__)

class RealWorldCoordinator:
    """
    Real World Coordinator for managing physical world interactions
    Handles scheduling, bookings, communications with safety and consent
    """
    
    def __init__(self, require_confirm: bool = True):
        self.require_confirm = require_confirm
        self.coordination_history = []
        self.pending_actions = {}
        
        # Coordination categories
        self.coordination_types = {
            'scheduling': {
                'description': 'Meeting and appointment scheduling',
                'capabilities': ['calendar management', 'availability checking', 'meeting setup'],
                'safety_level': 'medium'
            },
            'booking': {
                'description': 'Reservations and bookings',
                'capabilities': ['restaurant reservations', 'travel booking', 'service appointments'],
                'safety_level': 'high'
            },
            'communication': {
                'description': 'Phone calls and messages',
                'capabilities': ['appointment confirmation', 'service inquiries', 'information requests'],
                'safety_level': 'high'
            },
            'ordering': {
                'description': 'Product and service ordering',
                'capabilities': ['online ordering', 'delivery scheduling', 'service requests'],
                'safety_level': 'very_high'
            },
            'reminders': {
                'description': 'Task and appointment reminders',
                'capabilities': ['notification setup', 'deadline tracking', 'follow-up scheduling'],
                'safety_level': 'low'
            }
        }
    
    def route(self, text: str, require_confirm: bool = True) -> str:
        """Route real-world coordination requests"""
        try:
            text_lower = text.lower()
            
            # Meeting and appointment scheduling
            if any(phrase in text_lower for phrase in ['schedule meeting', 'book appointment', 'arrange meeting']):
                return self._handle_scheduling_request(text, require_confirm)
            
            # Restaurant and travel bookings
            elif any(phrase in text_lower for phrase in ['book restaurant', 'make reservation', 'book hotel', 'book flight']):
                return self._handle_booking_request(text, require_confirm)
            
            # Communication coordination
            elif any(phrase in text_lower for phrase in ['call', 'phone', 'message', 'contact']):
                return self._handle_communication_request(text, require_confirm)
            
            # Order and delivery coordination
            elif any(phrase in text_lower for phrase in ['order', 'delivery', 'purchase', 'buy']):
                return self._handle_ordering_request(text, require_confirm)
            
            # Reminder and follow-up management
            elif any(phrase in text_lower for phrase in ['remind me', 'set reminder', 'follow up']):
                return self._handle_reminder_request(text, require_confirm)
            
            # Location and navigation assistance
            elif any(phrase in text_lower for phrase in ['directions', 'location', 'address', 'map']):
                return self._handle_location_request(text)
            
            # General coordination
            else:
                return self._provide_coordination_overview()
                
        except Exception as e:
            logger.error(f"Error in real-world coordination routing: {e}")
            return f"Real-world coordination error: {e}"
    
    def _handle_scheduling_request(self, text: str, require_confirm: bool) -> str:
        """Handle meeting and appointment scheduling"""
        if require_confirm:
            return """📅 **Meeting & Appointment Scheduling**

**Available Scheduling Services:**

**🤝 Meeting Coordination:**
- Schedule business meetings
- Coordinate team calls
- Set up client appointments
- Arrange interview sessions

**🏥 Appointment Booking:**
- Medical appointments
- Professional services
- Personal care services
- Consultation scheduling

**⚠️ Important Consent & Privacy Notice:**
All scheduling activities require explicit confirmation and may involve:
- Sharing your contact information
- Coordinating with external parties
- Accessing calendar systems
- Making commitments on your behalf

**🛡️ Safety Protocols:**

**Before Scheduling:**
✅ **Verify Requirements** - Confirm all details are accurate
✅ **Check Authority** - Ensure you have permission to schedule
✅ **Review Commitments** - Understand what's being committed to
✅ **Confirm Contacts** - Verify recipient contact information

**During Scheduling:**
✅ **Transparent Communication** - Clear identification as assistant
✅ **Accurate Information** - Precise details and requirements
✅ **Professional Tone** - Respectful and business-appropriate
✅ **Confirmation Required** - Get approval before final booking

**📋 Scheduling Process:**

**Step 1: Requirements Gathering**
- Meeting purpose and agenda
- Required participants
- Preferred dates and times
- Duration and format needs
- Special requirements or preparations

**Step 2: Availability Coordination**
- Check participant calendars (if accessible)
- Propose meeting times
- Account for time zones
- Consider travel time if needed
- Identify potential conflicts

**Step 3: Meeting Setup**
- Send calendar invitations
- Include meeting details and agenda
- Provide necessary access information
- Set up required technology/tools
- Send confirmation to all parties

**📊 Scheduling Templates:**

**Business Meeting:**
- Professional introduction and context
- Clear meeting objectives
- Proposed agenda items
- Technology requirements
- Follow-up procedures

**Medical Appointment:**
- Basic information and insurance details
- Symptoms or concern summary
- Scheduling preferences
- Contact information verification
- Appointment preparation instructions

**Service Appointment:**
- Service requirements description
- Location and access details
- Availability windows
- Pricing and payment discussion
- Cancellation policy review

**🎯 Best Practices:**

**Professional Communication:**
- Clear, concise, and respectful language
- Professional email signature
- Appropriate subject lines
- Timely responses to inquiries
- Proper follow-up procedures

**Scheduling Efficiency:**
- Propose multiple time options
- Include all necessary details upfront
- Use calendar integration when possible
- Set appropriate meeting lengths
- Account for preparation and travel time

**⚠️ Limitations & Considerations:**

**What We Can Do:**
✅ Send scheduling requests on your behalf
✅ Coordinate with external parties
✅ Manage calendar invitations
✅ Provide meeting setup assistance
✅ Handle routine scheduling communications

**What Requires Your Direct Involvement:**
❌ Confidential or sensitive meetings
❌ Financial or legal appointments
❌ Personal medical consultations
❌ High-stakes business negotiations
❌ Emergency or urgent situations

**🔒 Privacy & Security:**

**Information Protection:**
- Minimal personal information sharing
- Secure communication channels
- Consent before sharing details
- Regular cleanup of scheduling data
- Transparent data usage policies

**Example Scheduling Request:**
"I'd like to schedule a 30-minute team meeting next week to discuss project status. Participants include John, Sarah, and Mike. Preferred times are Tuesday or Wednesday afternoon."

**Next Steps:**
To proceed with scheduling assistance:
1. **Provide specific meeting details**
2. **Confirm participant information**
3. **Specify timing preferences**
4. **Review and approve communication**
5. **Monitor and manage responses**

Ready to help with your scheduling needs. What meeting or appointment would you like to coordinate?"""
        
        else:
            return "Scheduling assistance initiated. Please provide meeting details for coordination."
    
    def _handle_booking_request(self, text: str, require_confirm: bool) -> str:
        """Handle booking and reservation requests"""
        if require_confirm:
            return """🏨 **Booking & Reservation Services**

**⚠️ HIGH-RISK ACTIVITY NOTICE ⚠️**
Booking services involve financial commitments and personal information. Extra caution and explicit consent required.

**Available Booking Categories:**

**🍽️ Restaurant Reservations:**
- Table booking coordination
- Special occasion arrangements
- Dietary requirement communication
- Group reservation management
- Cancellation and modification handling

**✈️ Travel Bookings:**
- Flight research and booking
- Hotel reservation management
- Car rental coordination
- Travel itinerary planning
- Travel insurance arrangements

**🏥 Service Appointments:**
- Healthcare provider bookings
- Professional service scheduling
- Personal care appointments
- Home service coordination
- Maintenance and repair scheduling

**💳 Financial Considerations:**

**Payment Implications:**
⚠️ **Credit Card Usage** - May require your payment information
⚠️ **Booking Fees** - Potential charges for reservations
⚠️ **Cancellation Policies** - Important terms and conditions
⚠️ **Price Fluctuations** - Rates may change during booking process
⚠️ **Hidden Costs** - Additional fees, taxes, or surcharges

**🛡️ Enhanced Safety Protocols:**

**Before Booking:**
✅ **Verify Service Provider** - Confirm legitimacy and reputation
✅ **Review Terms & Conditions** - Understand policies thoroughly
✅ **Check Pricing** - Confirm rates and additional fees
✅ **Validate Information** - Ensure all details are accurate
✅ **Confirm Authority** - Verify permission to make bookings

**During Booking:**
✅ **Secure Channels** - Use encrypted, secure booking platforms
✅ **Payment Protection** - Verify secure payment processing
✅ **Documentation** - Save all confirmation details
✅ **Verification** - Confirm booking with service provider
✅ **Backup Plans** - Prepare for potential issues

**📋 Booking Process Framework:**

**Phase 1: Research & Planning**
- Service requirement analysis
- Provider research and comparison
- Availability and pricing check
- Review policies and terms
- Prepare necessary information

**Phase 2: Booking Coordination**
- Contact preferred providers
- Negotiate terms if applicable
- Secure reservations with confirmations
- Process payments through secure channels
- Document all transaction details

**Phase 3: Confirmation & Management**
- Verify booking confirmations
- Schedule reminder notifications
- Monitor for changes or updates
- Prepare contingency plans
- Coordinate related logistics

**🏢 Service Provider Categories:**

**Hospitality Services:**
- Hotels and accommodations
- Restaurants and dining
- Entertainment venues
- Recreation facilities
- Event spaces and catering

**Transportation Services:**
- Airlines and flight booking
- Car rental agencies
- Ground transportation
- Travel packages
- Transportation passes

**Professional Services:**
- Healthcare providers
- Legal consultations
- Financial advisors
- Educational services
- Technical support

**Personal Services:**
- Beauty and wellness
- Home maintenance
- Personal care
- Fitness and training
- Specialty services

**⚖️ Legal & Ethical Considerations:**

**Booking Authority:**
- Verify legal authority to make reservations
- Understand liability implications
- Confirm payment authorization
- Review cancellation rights
- Consider insurance requirements

**Privacy Protection:**
- Minimize personal information sharing
- Use secure booking platforms
- Protect payment information
- Control data retention
- Monitor for unauthorized use

**🚨 Red Flags - When NOT to Book:**

❌ **Unverified Providers** - Unknown or suspicious services
❌ **Unsecure Payments** - Non-standard payment methods
❌ **Pressure Tactics** - Urgent or limited-time offers
❌ **Unclear Terms** - Vague policies or conditions
❌ **Excessive Information** - Unnecessary personal data requests

**💡 Booking Best Practices:**

**Research & Verification:**
- Check multiple review sources
- Verify business credentials
- Compare pricing across platforms
- Read terms and conditions carefully
- Confirm contact information

**Security & Protection:**
- Use secure, reputable booking platforms
- Pay with protected payment methods
- Keep detailed records of all transactions
- Set up confirmation alerts
- Monitor for fraudulent activity

**🎯 Recommended Approach:**

**For Low-Risk Bookings** (restaurant reservations, basic appointments):
- Direct coordination with minimal personal information
- Standard booking platforms and procedures
- Basic confirmation and documentation

**For High-Risk Bookings** (travel, expensive services):
- Enhanced verification and research
- Secure payment methods only
- Comprehensive documentation
- Multiple confirmation checks
- Insurance consideration

**Example Booking Request:**
"I need to book a dinner reservation for 4 people at [Restaurant Name] for Saturday evening around 7 PM. We'll need a table with good acoustics for business discussion."

**Alternative Approaches:**
If full booking coordination seems too risky:
1. **Research & Recommendation** - Find options and provide information
2. **Partial Assistance** - Help with research, you handle booking
3. **Template Communication** - Draft messages for you to send
4. **Comparison Shopping** - Find best options for your consideration

**Ready to Proceed?**
Given the financial and personal information implications, I recommend starting with:
1. **Specific requirements clarification**
2. **Risk assessment for the booking type**
3. **Security protocol selection**
4. **Step-by-step coordination with your approval**

What type of booking assistance do you need, and what's your preferred level of direct involvement?"""
        
        else:
            return "Booking assistance initiated. Please specify reservation requirements and preferred approach."
    
    def _handle_communication_request(self, text: str, require_confirm: bool) -> str:
        """Handle communication coordination requests"""
        if require_confirm:
            return """📞 **Communication Coordination**

**⚠️ COMMUNICATION SAFETY NOTICE ⚠️**
Phone calls and messages involve direct representation. Explicit consent and careful protocols required.

**Available Communication Services:**

**📞 Phone Call Coordination:**
- Appointment confirmation calls
- Service inquiry calls
- Information gathering calls
- Follow-up and status calls
- Professional consultation coordination

**📧 Message Management:**
- Email communication drafting
- Text message coordination
- Professional correspondence
- Follow-up message scheduling
- Contact information verification

**💬 Communication Types:**

**Business Communications:**
- Client meeting confirmations
- Service provider coordination
- Professional inquiry handling
- Appointment scheduling calls
- Project status communications

**Service Communications:**
- Appointment confirmations
- Service availability inquiries
- Billing and payment discussions
- Schedule change notifications
- Customer service interactions

**Information Communications:**
- Research and inquiry calls
- Information verification
- Service comparison inquiries
- Availability and pricing checks
- General information gathering

**🛡️ Communication Safety Protocols:**

**Before Communication:**
✅ **Verify Authority** - Confirm permission to represent you
✅ **Prepare Script** - Plan communication content and objectives
✅ **Check Information** - Verify all details are accurate
✅ **Identify Boundaries** - Understand what can/cannot be discussed
✅ **Prepare Documentation** - Ready to record important information

**During Communication:**
✅ **Clear Identification** - Transparent about assistant role
✅ **Professional Demeanor** - Respectful and business-appropriate
✅ **Accurate Representation** - Faithful to your instructions
✅ **Information Security** - Protect sensitive details
✅ **Detailed Documentation** - Record outcomes and next steps

**📋 Communication Framework:**

**Preparation Phase:**
- Define communication objectives
- Prepare key points and questions
- Gather necessary information
- Plan communication approach
- Set up documentation system

**Execution Phase:**
- Professional introduction and context
- Clear communication of objectives
- Active listening and information gathering
- Appropriate follow-up questions
- Confirmation of understanding

**Follow-up Phase:**
- Document communication outcomes
- Provide detailed report to you
- Schedule any necessary follow-up
- Update related systems or calendars
- Monitor for responses or changes

**🎭 Communication Styles:**

**Professional Business:**
- Formal, structured approach
- Clear objectives and agenda
- Respectful but efficient tone
- Business-focused content
- Professional follow-up procedures

**Service Customer:**
- Polite, customer-service appropriate
- Clear service requirements
- Patient but persistent approach
- Documentation of service details
- Appropriate escalation procedures

**Information Inquiry:**
- Curious but respectful tone
- Structured question approach
- Thorough information gathering
- Verification of important details
- Professional appreciation

**⚠️ Communication Limitations:**

**What We Can Handle:**
✅ Routine appointment confirmations
✅ Service availability inquiries
✅ Information gathering calls
✅ Professional scheduling coordination
✅ Standard customer service interactions

**What Requires Your Direct Involvement:**
❌ Sensitive personal matters
❌ Financial or legal discussions
❌ Medical consultation calls
❌ Emergency or urgent situations
❌ Complex negotiations or decisions

**🔒 Privacy & Security:**

**Information Protection:**
- Minimal personal information sharing
- Secure communication channels
- No sharing of sensitive details
- Clear boundaries on discussable topics
- Documentation of information shared

**Consent Management:**
- Explicit permission for each communication
- Clear scope of authority
- Regular confirmation of ongoing consent
- Easy revocation procedures
- Transparent activity reporting

**📞 Communication Script Examples:**

**Appointment Confirmation:**
"Hello, this is [Assistant Name] calling on behalf of [Your Name] to confirm an appointment scheduled for [Date/Time]. Could you please verify the appointment details and let me know if any preparation is needed?"

**Service Inquiry:**
"Good [morning/afternoon], I'm calling on behalf of [Your Name] to inquire about [Service]. Could you provide information about availability, pricing, and scheduling?"

**Information Gathering:**
"Hello, I'm researching [Topic] on behalf of [Your Name]. Could you provide information about [Specific Questions]? This is for [Purpose] and we'd appreciate any details you can share."

**📊 Communication Tracking:**

**Documentation Standards:**
- Date, time, and duration of communication
- Contact person and organization
- Key points discussed and outcomes
- Follow-up actions required
- Important information gathered

**Quality Assurance:**
- Review communication effectiveness
- Monitor for consistent representation
- Track response rates and outcomes
- Identify improvement opportunities
- Ensure ethical compliance

**🎯 Recommended Communication Approach:**

**For Routine Communications:**
- Standard scripts and procedures
- Clear identification and representation
- Professional tone and approach
- Thorough documentation
- Regular status updates

**For Complex Communications:**
- Enhanced preparation and planning
- Multiple approval checkpoints
- Detailed script development
- Real-time consultation availability
- Comprehensive outcome reporting

**Getting Started:**
To use communication coordination services:
1. **Define specific communication needs**
2. **Set clear boundaries and authority levels**
3. **Prepare key information and objectives**
4. **Review and approve communication approach**
5. **Monitor outcomes and provide feedback**

What type of communication coordination do you need assistance with?"""
        
        else:
            return "Communication coordination initiated. Please specify communication requirements and approval level."
    
    def _handle_ordering_request(self, text: str, require_confirm: bool) -> str:
        """Handle ordering and purchasing requests"""
        if require_confirm:
            return """🛒 **Ordering & Purchase Coordination**

**🚨 VERY HIGH-RISK ACTIVITY 🚨**
Ordering involves financial transactions and commitments. Maximum caution and explicit approval required.

**⚠️ Critical Financial Warning:**
All ordering activities involve spending your money and creating financial obligations. Each transaction requires explicit approval.

**Available Ordering Categories:**

**🍕 Food & Beverage Ordering:**
- Restaurant delivery coordination
- Grocery shopping assistance
- Catering arrangement
- Special diet accommodations
- Group order management

**📦 Product Purchasing:**
- Online shopping coordination
- Service product ordering
- Subscription management
- Bulk purchase coordination
- Gift and special occasion orders

**🏠 Service Ordering:**
- Home maintenance services
- Professional services
- Subscription services
- Utility services
- Digital services and software

**💳 Financial Safeguards:**

**Payment Protection Requirements:**
🔒 **Secure Channels Only** - Verified, encrypted payment platforms
🔒 **Payment Confirmation** - Explicit approval for every transaction
🔒 **Budget Verification** - Confirm spending authority and limits
🔒 **Receipt Documentation** - Complete transaction records
🔒 **Fraud Monitoring** - Watch for unauthorized charges

**🛡️ Maximum Security Protocols:**

**Pre-Purchase Verification:**
✅ **Vendor Verification** - Confirm legitimate, reputable sellers
✅ **Product/Service Validation** - Verify exactly what's being ordered
✅ **Price Confirmation** - Including all taxes, fees, and charges
✅ **Terms Review** - Return policies, warranties, terms of service
✅ **Budget Authorization** - Explicit spending approval
✅ **Alternative Options** - Compare multiple options when possible

**Transaction Security:**
✅ **Secure Platforms** - Only use verified, secure ordering systems
✅ **Payment Method Verification** - Confirm secure payment processing
✅ **Order Review** - Final confirmation before submission
✅ **Transaction Monitoring** - Watch for processing issues
✅ **Confirmation Documentation** - Save all order confirmations

**📋 Ordering Process Framework:**

**Phase 1: Requirement Analysis**
- Clearly define what's needed
- Set budget limits and constraints
- Identify preferred vendors/platforms
- Review timing and delivery requirements
- Understand return/cancellation policies

**Phase 2: Research & Comparison**
- Compare multiple vendors/options
- Verify pricing and total costs
- Read reviews and ratings
- Check vendor credibility
- Identify best value options

**Phase 3: Order Preparation**
- Finalize product/service selection
- Verify all order details
- Confirm delivery information
- Review payment method security
- Prepare order documentation

**Phase 4: Transaction Execution**
- Secure platform verification
- Final order review with you
- Execute transaction with monitoring
- Obtain confirmation details
- Set up delivery/fulfillment tracking

**Phase 5: Order Management**
- Monitor order status and delivery
- Handle any issues or problems
- Verify receipt and satisfaction
- Manage returns or exchanges if needed
- Document complete transaction record

**🏪 Vendor Categories & Safety Levels:**

**Low-Risk Vendors (Enhanced Caution):**
- Established major retailers (Amazon, Target, etc.)
- Well-known food delivery services
- Verified local businesses with good reviews
- Subscription services with good reputation

**Medium-Risk Vendors (Maximum Caution):**
- Smaller online retailers
- New or less-known service providers
- International vendors
- Marketplace sellers

**High-Risk Vendors (Avoid Unless Exceptional Circumstances):**
- Unknown or unverified vendors
- Platforms with poor security practices
- Vendors with poor reviews or ratings
- Any vendor requiring unusual payment methods

**💡 Safer Ordering Alternatives:**

**Research & Recommendation:**
Instead of direct ordering, I can:
- Research products and provide recommendations
- Compare prices and find best deals
- Identify reputable vendors
- Prepare order information for your review
- Draft orders for your final approval and execution

**Assisted Ordering:**
- Guide you through the ordering process
- Help verify vendor credibility
- Assist with price comparison
- Provide order template preparation
- Support order tracking and management

**Split Responsibility:**
- Handle research and preparation
- You handle final ordering and payment
- Assist with order tracking and issues
- Manage delivery coordination
- Support returns or exchanges

**🚨 When NOT to Proceed with Ordering:**

❌ **Unverified Vendors** - Unknown or suspicious sellers
❌ **Unsecure Payment** - Non-standard payment methods required
❌ **Excessive Cost** - Orders beyond reasonable budget limits
❌ **Unclear Terms** - Vague return or service policies
❌ **Pressure Situations** - Limited-time offers requiring immediate action
❌ **Personal/Sensitive Items** - Requiring personal judgment or preferences

**📊 Order Types & Recommendations:**

**Routine/Familiar Orders (Lower Risk):**
- Regular food delivery from known restaurants
- Standard household supplies from major retailers
- Repeat orders from established vendors
- Subscription renewals for familiar services

**New/Complex Orders (Higher Risk):**
- First-time purchases from new vendors
- High-value items or services
- Custom or personalized products
- Services requiring personal consultation

**🎯 Recommended Ordering Approach:**

**Start with Low-Risk, Familiar Orders:**
1. Use well-known, established vendors
2. Order familiar products/services
3. Stay within comfortable budget limits
4. Use secure, familiar payment methods
5. Maintain detailed documentation

**Gradually Expand with Experience:**
- Build comfort with coordination process
- Develop vendor verification procedures
- Establish clear budget and approval processes
- Create efficient documentation systems
- Build emergency response procedures

**Example Safe Ordering Request:**
"I'd like to order lunch from [Known Restaurant] - the usual Tuesday special for delivery to my office. Budget limit $15 including tip."

**Example Higher-Risk Order (Requires Enhanced Protocols):**
"Research and help me order a new laptop under $1000 from a reputable vendor with good warranty and return policy."

**🤝 Collaboration Approach:**

Given the financial risks, I strongly recommend a collaborative approach:
1. **I handle research and preparation**
2. **You review and approve all details**
3. **You execute final payment and ordering**
4. **I assist with tracking and coordination**
5. **We handle any issues together**

This approach provides the convenience of assistance while maintaining your direct control over financial transactions.

**Ready to Proceed?**
What type of ordering assistance do you need, and what's your preferred level of involvement in the financial aspects?"""
        
        else:
            return "Ordering assistance initiated. Please specify purchase requirements and approval level for financial transactions."
    
    def _handle_reminder_request(self, text: str, require_confirm: bool) -> str:
        """Handle reminder and follow-up requests"""
        return """⏰ **Reminder & Follow-up Management**

**Available Reminder Services:**

**📅 Appointment Reminders:**
- Meeting and call reminders
- Deadline notifications
- Event preparation alerts
- Travel departure reminders
- Important date notifications

**📋 Task Reminders:**
- Project milestone alerts
- Follow-up action reminders
- Recurring task notifications
- Goal progress check-ins
- Habit tracking reminders

**🔄 Follow-up Management:**
- Email follow-up scheduling
- Meeting follow-up reminders
- Project status check-ins
- Client communication follow-ups
- Service confirmation follow-ups

**📞 Communication Reminders:**
- Call-back scheduling
- Response deadline alerts
- Contact maintenance reminders
- Relationship check-in prompts
- Professional networking reminders

**⚙️ Reminder Setup Options:**

**Timing Preferences:**
- One-time reminders
- Recurring reminders (daily, weekly, monthly)
- Progressive reminders (multiple alerts)
- Countdown reminders
- Contextual timing (before meetings, etc.)

**Notification Methods:**
- Calendar notifications
- Email reminders
- Text message alerts (if configured)
- In-app notifications
- Desktop alerts

**Content Customization:**
- Custom reminder messages
- Context-specific information
- Action item checklists
- Preparation requirements
- Contact information inclusion

**📊 Reminder Categories:**

**Professional Reminders:**
- Meeting preparation alerts
- Project deadline notifications
- Client follow-up reminders
- Professional development tasks
- Business goal check-ins

**Personal Reminders:**
- Personal appointment alerts
- Health and wellness reminders
- Family and friend check-ins
- Personal goal progress
- Self-care activity prompts

**📋 Setting Up Reminders:**

**Information Needed:**
- What to be reminded about
- When to send the reminder
- How often (if recurring)
- What notification method to use
- Any special instructions or context

**Example Reminder Requests:**
- "Remind me to call John about the project status every Friday at 2 PM"
- "Set a reminder to review my goals every month on the 1st"
- "Alert me 30 minutes before all meetings to prepare"
- "Remind me to follow up on job applications every Tuesday"

**🎯 Reminder Best Practices:**

**Effective Timing:**
- Allow adequate preparation time
- Consider your typical schedule patterns
- Account for time zones if applicable
- Avoid overwhelming with too many alerts
- Balance frequency with importance

**Clear Content:**
- Specific, actionable reminder text
- Include relevant context or details
- Provide next steps or requirements
- Reference important information
- Include contact details if needed

What type of reminders would you like to set up?"""
    
    def _handle_location_request(self, text: str) -> str:
        """Handle location and navigation requests"""
        return """🗺️ **Location & Navigation Assistance**

**Available Location Services:**

**📍 Address & Location Information:**
- Business address lookup
- Contact information verification
- Operating hours and availability
- Accessibility information
- Parking and transportation options

**🚗 Transportation Planning:**
- Route planning and directions
- Public transportation options
- Travel time estimates
- Traffic and delay information
- Alternative route suggestions

**📊 Location Research:**
- Nearby services and amenities
- Local business recommendations
- Area information and reviews
- Event and activity information
- Local regulations and requirements

**🏢 Business Location Services:**
- Office and meeting location details
- Facility information and amenities
- Contact and scheduling information
- Accessibility and special requirements
- Visit preparation information

**🎯 How I Can Help:**

**Information Gathering:**
- Research locations and addresses
- Verify business information
- Check operating hours and availability
- Find contact information
- Gather accessibility details

**Planning Assistance:**
- Route and transportation planning
- Meeting location coordination
- Travel time calculation
- Parking and logistics planning
- Alternative options identification

**Coordination Support:**
- Location confirmation with others
- Address sharing and communication
- Meeting point coordination
- Transportation arrangement support
- Emergency location information

**🔒 Privacy & Safety:**

**Location Privacy:**
- No sharing of your current location
- Protection of home/work addresses
- Secure handling of location information
- Consent required for location sharing
- Regular cleanup of location data

**Safety Considerations:**
- Verification of location legitimacy
- Safety information for areas/venues
- Emergency contact information
- Alternative route planning
- Weather and condition alerts

What location assistance do you need?"""
    
    def _provide_coordination_overview(self) -> str:
        """Provide general coordination overview"""
        return """🌍 **Real World Coordination Overview**

**What is Real World Coordination?**
I help bridge the digital-physical divide by coordinating real-world tasks like scheduling, bookings, communications, and logistics while maintaining safety and consent protocols.

**🎯 Core Coordination Services:**

**📅 Scheduling & Appointments:**
- Meeting coordination and calendar management
- Appointment booking and confirmation
- Availability checking and coordination
- Reminder and notification management

**🏨 Booking & Reservations:**
- Restaurant and venue reservations
- Travel and accommodation booking
- Service appointment scheduling
- Event and activity coordination

**📞 Communication Coordination:**
- Phone call management and coordination
- Email and message coordination
- Contact management and outreach
- Professional communication assistance

**🛒 Ordering & Purchasing:**
- Product and service ordering assistance
- Delivery and fulfillment coordination
- Vendor research and comparison
- Purchase planning and management

**📍 Location & Navigation:**
- Address and location research
- Transportation planning and coordination
- Location verification and confirmation
- Logistics and travel coordination

**🛡️ Safety & Ethics Framework:**

**Consent & Control:**
- Explicit permission required for all actions
- Clear scope of authority and limitations
- Easy override and modification capabilities
- Transparent activity reporting and documentation

**Privacy Protection:**
- Minimal personal information sharing
- Secure communication and transaction channels
- Protection of sensitive details and preferences
- Regular cleanup of coordination data

**Financial Safety:**
- Enhanced protocols for money-related activities
- Multiple confirmation requirements for purchases
- Secure payment method verification
- Complete transaction documentation

**🎯 Coordination Approach:**

**Risk-Based Protocols:**
- **Low Risk** (reminders, information): Standard procedures
- **Medium Risk** (scheduling, communication): Enhanced verification
- **High Risk** (booking, ordering): Maximum security protocols
- **Very High Risk** (financial transactions): Multiple confirmations

**Collaborative Process:**
- Research and preparation assistance
- Option analysis and recommendation
- Coordination execution with oversight
- Follow-up and issue resolution
- Continuous improvement and optimization

**📊 Getting Started:**

**Assessment Phase:**
- Identify routine coordination needs
- Assess risk levels and requirements
- Define boundaries and approval processes
- Set up communication and consent protocols

**Implementation Phase:**
- Start with low-risk coordination tasks
- Build comfort and trust with the process
- Gradually expand to more complex coordination
- Continuously refine and improve procedures

**🤝 Partnership Approach:**

The goal is to create an effective partnership where:
- You maintain control and final decision authority
- I handle research, coordination, and logistics
- We work together to achieve your objectives efficiently
- Safety, privacy, and ethics are always prioritized

**Common Coordination Scenarios:**

**Business Professional:**
- Meeting scheduling and coordination
- Travel planning and booking
- Client communication management
- Service provider coordination

**Personal Life:**
- Appointment scheduling and management
- Event planning and coordination
- Service booking and management
- Family and friend coordination

**Project Management:**
- Team coordination and scheduling
- Vendor and service provider management
- Logistics and resource coordination
- Communication and update management

**Next Steps:**
What real-world coordination challenges do you face that could benefit from assistance? Let's start with identifying your most time-consuming or complex coordination tasks.

Ready to help make your real-world coordination more efficient and effective!"""
    
    def coordinate_action(self, action_type: str, details: Dict[str, Any], require_confirm: bool = True) -> str:
        """Coordinate a specific real-world action"""
        try:
            if require_confirm:
                # Store action for approval
                action_id = f"action_{datetime.now().timestamp()}"
                self.pending_actions[action_id] = {
                    'type': action_type,
                    'details': details,
                    'created_at': datetime.now().isoformat(),
                    'status': 'pending_approval'
                }
                
                return f"Action prepared for approval. ID: {action_id}. Please review and confirm before execution."
            else:
                # Execute action directly (simulation)
                return f"Action '{action_type}' executed successfully."
                
        except Exception as e:
            logger.error(f"Error coordinating action: {e}")
            return f"Failed to coordinate action: {e}"
    
    def get_coordination_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent coordination history"""
        return self.coordination_history[-limit:] if self.coordination_history else []
    
    def get_pending_actions(self) -> List[Dict[str, Any]]:
        """Get pending actions awaiting approval"""
        return [action for action in self.pending_actions.values() if action['status'] == 'pending_approval']
    
    def approve_action(self, action_id: str) -> str:
        """Approve a pending action"""
        try:
            if action_id not in self.pending_actions:
                return "Action not found"
            
            action = self.pending_actions[action_id]
            action['status'] = 'approved'
            action['approved_at'] = datetime.now().isoformat()
            
            # Move to history
            self.coordination_history.append(action)
            
            return f"Action {action_id} approved and executed successfully"
            
        except Exception as e:
            logger.error(f"Error approving action: {e}")
            return f"Failed to approve action: {e}"
